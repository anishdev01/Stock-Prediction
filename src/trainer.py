# ══════════════════════════════════════════════════════════════════════════════
#  TASK 3 — MODEL TRAINER (UPGRADED)
#  Three advanced ML models: Linear Regression, Ridge Regression, LSTM
#  Indian Stock Predictor · Alpha Five Team · Brainware University
# ══════════════════════════════════════════════════════════════════════════════

import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# TensorFlow/Keras for LSTM
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    from tensorflow.keras.callbacks import EarlyStopping
    KERAS_AVAILABLE = True
except ImportError:
    KERAS_AVAILABLE = False
    print("⚠️  TensorFlow not installed. LSTM will be skipped.")


# ── Model definitions ───────────────────────────────────────────────────────

def _make_models():
    """Returns dictionary of sklearn model objects"""
    return {
        # 1. Linear Regression (baseline)
        "Linear Regression": LinearRegression(),
        
        # 2. Ridge Regression (L2 regularization to prevent overfitting)
        "Ridge Regression": Ridge(alpha=10.0, fit_intercept=True),
    }


# ── Preprocessing ──────────────────────────────────────────────────────────

def preprocess(X_train_df: pd.DataFrame, X_test_df: pd.DataFrame):
    """
    1. Impute missing values with median
    2. Standardize to zero-mean, unit-variance
    Fit ONLY on train data to prevent leakage.
    """
    imputer = SimpleImputer(strategy="median")
    scaler = StandardScaler()

    X_tr = scaler.fit_transform(imputer.fit_transform(X_train_df))
    X_te = scaler.transform(imputer.transform(X_test_df))

    return X_tr, X_te, imputer, scaler


# ── LSTM Model Builder ─────────────────────────────────────────────────────

def build_lstm_model(input_shape, units=50):
    """
    Builds a simple LSTM model for time series prediction
    """
    if not KERAS_AVAILABLE:
        return None
        
    model = Sequential([
        LSTM(units, activation='relu', return_sequences=True, input_shape=input_shape),
        Dropout(0.2),
        LSTM(units//2, activation='relu'),
        Dropout(0.2),
        Dense(25, activation='relu'),
        Dense(1)
    ])
    
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model


def reshape_for_lstm(X, lookback=10):
    """
    Reshape 2D data (samples, features) to 3D (samples, timesteps, features)
    Uses a sliding window approach
    """
    if len(X) < lookback:
        lookback = max(1, len(X) // 2)
    
    samples = []
    targets = []
    
    for i in range(lookback, len(X)):
        samples.append(X[i-lookback:i])
        targets.append(X[i, 0])  # Assuming first column is the target
    
    return np.array(samples), np.array(targets)


# ── Main training function ─────────────────────────────────────────────────

def train_all(X_train: np.ndarray, y_train: np.ndarray,
              X_test: np.ndarray, y_test: np.ndarray,
              feature_names: list = None):
    """
    Trains all three models and returns diagnostics.

    Returns
    -------
    performance : DataFrame  — RMSE, MAE, R² per model
    models      : dict       — fitted model objects
    test_preds  : dict       — predictions on test set
    feat_imp    : dict       — feature importances (if available)
    """
    sklearn_models = _make_models()
    rows, trained, test_preds, feat_imp = [], {}, {}, {}

    # Train sklearn models (Linear & Ridge)
    for name, model in sklearn_models.items():
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
        mae = float(mean_absolute_error(y_test, y_pred))
        r2 = float(r2_score(y_test, y_pred))

        rows.append({
            "Model": name,
            "RMSE": rmse,
            "MAE": mae,
            "R²": r2,
        })
        trained[name] = model
        test_preds[name] = y_pred.tolist()
        
        # Linear/Ridge have coefficients, not feature importance
        if hasattr(model, 'coef_') and feature_names:
            coef = pd.Series(np.abs(model.coef_), index=feature_names)
            feat_imp[name] = coef.sort_values(ascending=False).head(10).to_dict()

    # Train LSTM model
    if KERAS_AVAILABLE and len(X_train) > 20:
        try:
            lookback = min(10, len(X_train) // 5)
            
            # Reshape data for LSTM
            X_train_lstm, y_train_lstm = reshape_for_lstm(X_train, lookback)
            X_test_lstm, y_test_lstm = reshape_for_lstm(X_test, lookback)
            
            if len(X_train_lstm) > 10:
                lstm_model = build_lstm_model(
                    input_shape=(X_train_lstm.shape[1], X_train_lstm.shape[2])
                )
                
                early_stop = EarlyStopping(monitor='val_loss', patience=5, 
                                          restore_best_weights=True)
                
                lstm_model.fit(
                    X_train_lstm, y_train_lstm,
                    epochs=50, batch_size=16,
                    validation_split=0.1,
                    callbacks=[early_stop],
                    verbose=0
                )
                
                y_pred_lstm = lstm_model.predict(X_test_lstm, verbose=0).flatten()
                
                rmse = float(np.sqrt(mean_squared_error(y_test_lstm, y_pred_lstm)))
                mae = float(mean_absolute_error(y_test_lstm, y_pred_lstm))
                r2 = float(r2_score(y_test_lstm, y_pred_lstm))

                rows.append({
                    "Model": "LSTM",
                    "RMSE": rmse,
                    "MAE": mae,
                    "R²": r2,
                })
                trained["LSTM"] = lstm_model
                # Align predictions with test set length
                pred_aligned = [None] * (len(y_test) - len(y_pred_lstm)) + y_pred_lstm.tolist()
                test_preds["LSTM"] = pred_aligned
                
        except Exception as e:
            print(f"⚠️  LSTM training failed: {e}")

    perf = (pd.DataFrame(rows)
              .set_index("Model")
              .sort_values("RMSE"))

    return perf, trained, test_preds, feat_imp


# ── Confidence interval from test residuals ────────────────────────────────

def residual_std(test_preds: dict, y_test: np.ndarray) -> dict:
    """
    Computes standard deviation of residuals on test set
    """
    result = {}
    for name, preds in test_preds.items():
        # Filter out None values for LSTM alignment
        valid_preds = [p for p in preds if p is not None]
        valid_test = y_test[-len(valid_preds):]
        
        if len(valid_preds) > 0:
            residuals = np.array(valid_preds) - valid_test
            result[name] = float(np.std(residuals))
        else:
            result[name] = 0.0
    return result
