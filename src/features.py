# ══════════════════════════════════════════════════════════════════════════════
#  TASK 2 — FEATURE ENGINEERING
#  Builds a rich but disciplined set of technical indicators.
#  Anti-overfit design: every feature has a clear market rationale.
#  Indian Stock Predictor · Alpha Five Team · Brainware University
# ══════════════════════════════════════════════════════════════════════════════

import numpy as np
import pandas as pd


# ── Helpers ────────────────────────────────────────────────────────────────

def _rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain  = delta.clip(lower=0).rolling(period, min_periods=period // 2).mean()
    loss  = (-delta.clip(upper=0)).rolling(period, min_periods=period // 2).mean()
    rs    = gain / loss.replace(0, np.nan)
    return (100 - 100 / (1 + rs)).fillna(50)


def _stochastic(high: pd.Series, low: pd.Series, close: pd.Series,
                k_period: int = 14, d_period: int = 3):
    """Stochastic Oscillator %K and %D — momentum / overbought signal."""
    lowest_low   = low.rolling(k_period, min_periods=k_period // 2).min()
    highest_high = high.rolling(k_period, min_periods=k_period // 2).max()
    denom = (highest_high - lowest_low).replace(0, np.nan)
    k = 100 * (close - lowest_low) / denom
    d = k.rolling(d_period).mean()
    return k.fillna(50), d.fillna(50)


def _atr(high: pd.Series, low: pd.Series, close: pd.Series,
         period: int = 14) -> pd.Series:
    """Average True Range — measures price volatility."""
    prev_close = close.shift(1)
    tr = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low  - prev_close).abs(),
    ], axis=1).max(axis=1)
    return tr.rolling(period, min_periods=period // 2).mean()


def _obv(close: pd.Series, volume: pd.Series) -> pd.Series:
    """On-Balance Volume — volume-price trend indicator."""
    direction = np.sign(close.diff()).fillna(0)
    return (direction * volume).cumsum()


# ══════════════════════════════════════════════════════════════════════════════

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds 18 carefully selected technical indicators.

    Group           Feature         Why it matters
    ─────────────── ─────────────── ────────────────────────────────────────────
    Trend           SMA 20 / 50     Short & medium-term trend direction
    Trend           EMA 20          Reacts faster to recent price changes
    Trend momentum  MACD / Signal   Crossover signals shift in momentum
    Momentum        RSI 14          Identifies overbought / oversold conditions
    Momentum        Stoch %K / %D   Confirms RSI; detects reversals
    Volatility      Bollinger %B    Where price sits in its volatility band
    Volatility      ATR 14          Absolute price swing size
    Volatility      Rolling Std     20-day standard deviation of returns
    Volume          OBV             Confirms price moves with volume
    Volume          Volume Ratio    Detects unusual buying / selling activity
    Returns         Daily Return    Percentage change today
    Returns         ROC-5 / ROC-20  Rate of change: 1-week & 1-month
    Price memory    Lag 1 / 5 / 10  Yesterday, last week, 2 weeks ago
    """
    df    = df.copy()
    price = df["adj_close"] if "adj_close" in df.columns else df["close"]
    high  = df.get("high",  price)
    low   = df.get("low",   price)

    # ── Trend: Moving Averages ────────────────────────────────────────────
    df["sma_20"] = price.rolling(20, min_periods=10).mean()
    df["sma_50"] = price.rolling(50, min_periods=25).mean()
    df["ema_20"] = price.ewm(span=20, adjust=False).mean()

    # Price position relative to moving averages (normalised)
    df["price_vs_sma20"] = (price - df["sma_20"]) / df["sma_20"].replace(0, np.nan)

    # ── MACD ─────────────────────────────────────────────────────────────
    ema_12 = price.ewm(span=12, adjust=False).mean()
    ema_26 = price.ewm(span=26, adjust=False).mean()
    df["macd"]        = ema_12 - ema_26
    df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()
    df["macd_hist"]   = df["macd"] - df["macd_signal"]

    # ── RSI ───────────────────────────────────────────────────────────────
    df["rsi"] = _rsi(price, 14)

    # ── Stochastic Oscillator ─────────────────────────────────────────────
    df["stoch_k"], df["stoch_d"] = _stochastic(high, low, price)

    # ── Bollinger Bands ───────────────────────────────────────────────────
    bb_mid   = price.rolling(20, min_periods=10).mean()
    bb_std   = price.rolling(20, min_periods=10).std()
    bb_upper = bb_mid + 2 * bb_std
    bb_lower = bb_mid - 2 * bb_std
    df["bb_upper"] = bb_upper   # kept for charting only
    df["bb_lower"] = bb_lower   # kept for charting only
    bb_width = (bb_upper - bb_lower).replace(0, np.nan)
    df["bb_pct"]   = ((price - bb_lower) / bb_width).fillna(0.5)
    df["bb_width"] = (bb_width / bb_mid.replace(0, np.nan)).fillna(0)  # normalised bandwidth

    # ── ATR (Volatility) ──────────────────────────────────────────────────
    df["atr"] = _atr(high, low, price)
    df["atr_pct"] = (df["atr"] / price.replace(0, np.nan)).fillna(0)   # normalised ATR

    # ── Rolling volatility of returns ─────────────────────────────────────
    daily_ret = price.pct_change()
    df["daily_return"]  = daily_ret
    df["volatility_20"] = daily_ret.rolling(20, min_periods=10).std()

    # ── Volume features ───────────────────────────────────────────────────
    if "volume" in df.columns:
        vol = df["volume"]
        vol_ma = vol.rolling(10, min_periods=5).mean().replace(0, np.nan)
        df["volume_ratio"] = (vol / vol_ma).fillna(1)
        df["obv"] = _obv(price, vol)
        # Normalise OBV by its own rolling mean so scale doesn't leak info
        obv_ma = df["obv"].rolling(20, min_periods=10).mean().replace(0, np.nan)
        df["obv_norm"] = (df["obv"] / obv_ma.abs()).fillna(1)
    else:
        df["volume_ratio"] = 1.0
        df["obv_norm"]     = 1.0

    # ── Rate of Change ────────────────────────────────────────────────────
    df["roc_5"]  = price.pct_change(5)
    df["roc_20"] = price.pct_change(20)

    # ── Price lags ────────────────────────────────────────────────────────
    df["lag_1"]  = price.shift(1)
    df["lag_5"]  = price.shift(5)
    df["lag_10"] = price.shift(10)

    return df


# ══════════════════════════════════════════════════════════════════════════════

def build_xy(df: pd.DataFrame, target_col: str = "adj_close", shift_days: int = 1):
    """
    Constructs feature matrix X and target vector y.

    Target = closing price `shift_days` trading days into the future.
    Raw OHLCV columns are excluded to prevent data leakage.
    """
    df = df.copy()
    df["target"] = df[target_col].shift(-shift_days)
    df = df.dropna(subset=["target"])

    # Columns that must NOT be used as features
    exclude = {
        "target", "date",
        target_col, "open", "high", "low", "close",
        "volume",                     # raw volume → use ratio/OBV instead
        "bb_upper", "bb_lower",       # chart-only columns
        "obv",                        # use normalised version
    }
    feature_cols = [c for c in df.columns if c not in exclude]

    X = df[feature_cols].copy()
    y = df["target"].copy()

    # Drop rows where ANY feature is NaN
    valid = ~X.isna().any(axis=1)
    return X[valid], y[valid]


def time_split(df: pd.DataFrame, test_frac: float = 0.2):
    """
    Chronological train / test split — NEVER shuffle time-series data.
    The test set is always the most recent `test_frac` fraction of rows.
    """
    n = int(len(df) * (1 - test_frac))
    return df.iloc[:n].reset_index(drop=True), df.iloc[n:].reset_index(drop=True)
