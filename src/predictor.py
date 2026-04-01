# ══════════════════════════════════════════════════════════════════════════════
#  TASK 4 — PREDICTOR  (Full ML Pipeline Orchestrator)
#  Runs every step: fetch → engineer → split → scale → train → predict.
#  Prediction target is a specific DATE chosen by the user (no "days ahead").
#  Indian Stock Predictor · Alpha Five Team · Brainware University
# ══════════════════════════════════════════════════════════════════════════════

import numpy as np
import pandas as pd
from datetime import date, timedelta

from src.data_fetcher import fetch_stock_data
from src.features     import add_indicators, build_xy, time_split
from src.trainer      import preprocess, train_all, residual_std


# ── Utility: count trading days between two dates ──────────────────────────

def _trading_days_ahead(last_date: pd.Timestamp, target_date: pd.Timestamp) -> int:
    """
    Counts approximate trading days (Mon–Fri, ignoring Indian holidays)
    between `last_date` and `target_date`.  Returns at least 1.
    """
    if target_date <= last_date:
        return 1
    days = 0
    cur  = last_date + timedelta(days=1)
    while cur <= target_date:
        if cur.weekday() < 5:   # 0=Mon … 4=Fri
            days += 1
        cur += timedelta(days=1)
    return max(days, 1)


# ── Recursive multi-step prediction ───────────────────────────────────────

def _recursive_predict(models: dict, last_X_df: pd.DataFrame,
                       imputer, scaler, n_steps: int) -> dict:
    """
    Predicts `n_steps` trading days ahead using recursive forecasting.

    Strategy:
      • Step 1: predict from the last known features.
      • Steps 2…N: replace lag_1 with the previous prediction, then predict.
        All other features (RSI, MACD, volume, etc.) are held at their most
        recent observed values — a standard "frozen feature" approximation.

    This is honest about uncertainty: confidence degrades with horizon.
    """
    trajectories = {name: [] for name in models}

    current_df = last_X_df.copy()

    for step in range(n_steps):
        X_scaled = scaler.transform(imputer.transform(current_df))
        for name, model in models.items():
            pred = float(model.predict(X_scaled)[0])
            trajectories[name].append(pred)

        # Update price-memory features with the ensemble prediction of this step
        step_preds = [trajectories[n][-1] for n in models]
        ensemble_pred = float(np.mean(step_preds))

        if "lag_1" in current_df.columns:
            prev_lag1 = current_df["lag_1"].iloc[0]
            if "lag_5" in current_df.columns and step == 4:
                current_df["lag_5"] = prev_lag1
            if "lag_10" in current_df.columns and step == 9:
                current_df["lag_10"] = prev_lag1
            current_df["lag_1"] = ensemble_pred

        # Approximate daily_return with the implied change
        if "daily_return" in current_df.columns and "lag_1" in current_df.columns:
            prev = current_df["lag_1"].iloc[0]
            if prev != 0:
                current_df["daily_return"] = (ensemble_pred - prev) / prev

    # Return only the final-step prediction (the target date's price)
    return {name: round(traj[-1], 2) for name, traj in trajectories.items()}


# ══════════════════════════════════════════════════════════════════════════════

def run(ticker: str,
        prediction_date: str = None,
        lookback_days:   int   = 730,
        test_frac:       float = 0.2) -> dict:
    """
    Full ML pipeline.

    Parameters
    ----------
    ticker          : NSE ticker, e.g. "RELIANCE.NS"
    prediction_date : Date string "YYYY-MM-DD" for the price we want to predict
    lookback_days   : Calendar days of historical data to fetch
    test_frac       : Fraction of data reserved for the test set

    Returns
    -------
    A dict with everything the frontend needs to render results.
    """
    if prediction_date is None:
        prediction_date = str(date.today())

    # ── Step 1: Fetch historical data ─────────────────────────────────────
    df_raw = fetch_stock_data(ticker, prediction_date, lookback_days)

    # ── Step 2: Feature engineering ───────────────────────────────────────
    df = add_indicators(df_raw)

    target_col    = "adj_close" if "adj_close" in df.columns else "close"
    current_price = float(df[target_col].iloc[-1])
    last_date     = pd.to_datetime(df["date"].iloc[-1])
    pred_date_ts  = pd.to_datetime(prediction_date)

    # How many trading days until the requested prediction date?
    days_ahead = _trading_days_ahead(last_date, pred_date_ts)

    # ── Step 3: Train / test split ────────────────────────────────────────
    train_df, test_df = time_split(df, test_frac)

    # Always train models on 1-day-ahead (most data; lowest noise)
    X_tr_df, y_tr = build_xy(train_df, target_col, shift_days=1)
    X_te_df, y_te = build_xy(test_df,  target_col, shift_days=1)

    # Align feature columns (drop any that appear in only one split)
    shared_cols = sorted(set(X_tr_df.columns) & set(X_te_df.columns))
    X_tr_df, X_te_df = X_tr_df[shared_cols], X_te_df[shared_cols]

    # ── Step 4: Preprocessing ─────────────────────────────────────────────
    X_tr, X_te, imputer, scaler = preprocess(X_tr_df, X_te_df)

    # ── Step 5: Train all three models ────────────────────────────────────
    perf, models, test_preds, feat_imp = train_all(
        X_tr, y_tr.values, X_te, y_te.values,
        feature_names=shared_cols
    )

    # ── Step 6: Estimate prediction uncertainty from test residuals ────────
    res_std = residual_std(test_preds, y_te.values)

    # ── Step 7: Predict for the target date ───────────────────────────────
    # Use the last available row of features, then recurse for days_ahead steps
    last_row_df = X_te_df.iloc[[-1]].copy()
    if len(last_row_df) == 0:
        last_row_df = X_tr_df.iloc[[-1]].copy()

    if days_ahead == 1:
        # Simple direct 1-step prediction
        last_scaled = scaler.transform(imputer.transform(last_row_df))
        target_pred = {}
        for name, model in models.items():
            try:
                target_pred[name] = round(float(model.predict(last_scaled)[0]), 2)
            except Exception:
                target_pred[name] = None
    else:
        # Recursive multi-step prediction
        target_pred = _recursive_predict(models, last_row_df, imputer, scaler, days_ahead)

    # Widen confidence with horizon (each extra day adds ~1 residual-std)
    horizon_multiplier = 1.0 + 0.15 * (days_ahead - 1)   # conservative widening

    # Ensemble = weighted average (Ridge gets less weight for long horizons)
    valid_preds = [v for v in target_pred.values() if v is not None]
    ensemble    = round(float(np.mean(valid_preds)), 2) if valid_preds else None

    # Confidence band (±1σ × horizon factor, averaged across models)
    avg_std   = float(np.mean(list(res_std.values()))) if res_std else 0
    conf_band = round(avg_std * horizon_multiplier, 2)

    return {
        # Core dataframe (for charting)
        "df":               df,

        # Model evaluation
        "performance":      perf,
        "test_preds":       test_preds,
        "y_test":           y_te.tolist(),
        "test_start_idx":   len(train_df),

        # Feature importances
        "feat_imp":         feat_imp,

        # Predictions for the requested date
        "target_pred":      target_pred,
        "ensemble":         ensemble,
        "conf_band":        conf_band,
        "days_ahead":       days_ahead,
        "prediction_date":  prediction_date,

        # Metadata
        "current_price":    current_price,
        "last_date":        str(last_date.date()),
        "train_size":       len(X_tr),
        "test_size":        len(X_te),
        "feature_names":    shared_cols,
        "target":           target_col,
        "res_std":          res_std,
    }
