# ══════════════════════════════════════════════════════════════════════════════
#  TASK 3 — MODEL TRAINER
#  Three production-grade ML models with strong anti-overfit settings.
#  Validated with TimeSeriesSplit cross-validation (walk-forward).
#
#  Model          Why it's here
#  ─────────────  ────────────────────────────────────────────────────────────
#  Ridge Reg.     L2-regularised linear baseline; fast & interpretable
#  Gradient Boost Boosted shallow trees; best accuracy in most tabular tasks
#  Random Forest  Bagged deep trees; robust & naturally estimates uncertainty
#
#  Indian Stock Predictor · Alpha Five Team · Brainware University
# ══════════════════════════════════════════════════════════════════════════════

import numpy as np
import pandas as pd

from sklearn.linear_model    import Ridge
from sklearn.ensemble        import GradientBoostingRegressor, RandomForestRegressor
from sklearn.preprocessing   import StandardScaler
from sklearn.impute          import SimpleImputer
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics         import mean_squared_error, mean_absolute_error, r2_score


# ── Model definitions with carefully tuned anti-overfitting parameters ─────

def _make_models():
    return {
        # ── 1. Ridge Regression ──────────────────────────────────────────
        #    alpha=50: strong L2 penalty shrinks noisy coefficients toward 0.
        #    Prevents the linear model from fitting noise in financial data.
        "Ridge Regression": Ridge(alpha=50.0, fit_intercept=True),

        # ── 2. Gradient Boosting ─────────────────────────────────────────
        #    Many small steps (learning_rate=0.03) with shallow trees (depth=3).
        #    subsample=0.8 → stochastic boosting (like dropout for trees).
        #    min_samples_leaf=15 → each leaf must cover at least 15 days.
        "Gradient Boosting": GradientBoostingRegressor(
            n_estimators=300,
            learning_rate=0.03,
            max_depth=3,
            subsample=0.8,
            min_samples_leaf=15,
            max_features=0.7,
            validation_fraction=0.1,   # early-stopping holdout
            n_iter_no_change=25,       # stop if no improvement for 25 rounds
            tol=1e-4,
            random_state=42,
        ),

        # ── 3. Random Forest ─────────────────────────────────────────────
        #    Ensemble of 300 diverse trees via bagging + feature randomness.
        #    max_features='sqrt' ≈ each split sees √(n_features) features.
        #    min_samples_leaf=10 → smooth, generalisable leaf nodes.
        "Random Forest": RandomForestRegressor(
            n_estimators=300,
            max_depth=8,
            min_samples_leaf=10,
            max_features="sqrt",
            bootstrap=True,
            oob_score=True,      # out-of-bag estimate (free cross-validation)
            n_jobs=-1,
            random_state=42,
        ),
    }


# ── Preprocessing ──────────────────────────────────────────────────────────

def preprocess(X_train_df: pd.DataFrame, X_test_df: pd.DataFrame):
    """
    1. Impute missing values with the column median (fit on train only).
    2. Standardise to zero-mean, unit-variance   (fit on train only).

    Fitting ONLY on the training set prevents data leakage.
    """
    imputer = SimpleImputer(strategy="median")
    scaler  = StandardScaler()

    X_tr = scaler.fit_transform(imputer.fit_transform(X_train_df))
    X_te = scaler.transform(imputer.transform(X_test_df))

    return X_tr, X_te, imputer, scaler


# ── Walk-forward cross-validation ─────────────────────────────────────────

def _walk_forward_cv(model, X: np.ndarray, y: np.ndarray, n_splits: int = 5) -> float:
    """
    TimeSeriesSplit cross-validation:
      • Each fold always trains on the PAST and validates on the FUTURE.
      • Mimics real-world model deployment (no look-ahead bias).

    Returns mean RMSE across all folds.
    """
    tscv   = TimeSeriesSplit(n_splits=n_splits)
    errors = []
    for train_idx, val_idx in tscv.split(X):
        m = type(model)(**model.get_params())   # fresh copy each fold
        m.fit(X[train_idx], y[train_idx])
        preds = m.predict(X[val_idx])
        errors.append(float(np.sqrt(mean_squared_error(y[val_idx], preds))))
    return float(np.mean(errors))


# ── Main training function ─────────────────────────────────────────────────

def train_all(X_train: np.ndarray, y_train: np.ndarray,
              X_test:  np.ndarray, y_test:  np.ndarray,
              feature_names: list = None):
    """
    Trains all three models and returns rich diagnostics.

    Returns
    -------
    performance   : DataFrame  — RMSE, MAE, R², CV-RMSE per model
    models        : dict       — fitted model objects
    test_preds    : dict       — predictions on the held-out test set
    feat_imp      : dict       — feature importances (RF & GBR only)
    """
    models_def = _make_models()
    rows, trained, test_preds, feat_imp = [], {}, {}, {}

    for name, model in models_def.items():
        # ── Train ─────────────────────────────────────────────────────
        model.fit(X_train, y_train)

        # ── Test-set evaluation ───────────────────────────────────────
        y_pred = model.predict(X_test)
        rmse   = float(np.sqrt(mean_squared_error(y_test, y_pred)))
        mae    = float(mean_absolute_error(y_test, y_pred))
        r2     = float(r2_score(y_test, y_pred))

        # ── Walk-forward CV (on training data) ────────────────────────
        cv_rmse = _walk_forward_cv(model, X_train, y_train, n_splits=5)

        rows.append({
            "Model":   name,
            "RMSE":    rmse,
            "MAE":     mae,
            "R²":      r2,
            "CV-RMSE": cv_rmse,
        })
        trained[name]    = model
        test_preds[name] = y_pred.tolist()

        # ── Feature importance ────────────────────────────────────────
        if feature_names and hasattr(model, "feature_importances_"):
            fi = pd.Series(model.feature_importances_, index=feature_names)
            feat_imp[name] = fi.sort_values(ascending=False).head(10).to_dict()

    perf = (pd.DataFrame(rows)
              .set_index("Model")
              .sort_values("RMSE"))

    return perf, trained, test_preds, feat_imp


# ── Confidence interval from test residuals ────────────────────────────────

def residual_std(test_preds: dict, y_test: np.ndarray) -> dict:
    """
    Computes the standard deviation of residuals on the test set.
    Used to build ±1 / ±2 σ confidence bands for future predictions.
    """
    result = {}
    for name, preds in test_preds.items():
        residuals = np.array(preds) - y_test
        result[name] = float(np.std(residuals))
    return result
