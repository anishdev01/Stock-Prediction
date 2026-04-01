# ══════════════════════════════════════════════════════════════════════════════
#  TASK 5 — CHARTS  (Plotly JSON generators)
#  Returns Plotly figures as JSON strings for the browser.
#  Indian Stock Predictor · Alpha Five Team · Brainware University
# ══════════════════════════════════════════════════════════════════════════════

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ── Shared dark theme ──────────────────────────────────────────────────────

_BG   = "rgba(0,0,0,0)"
_GRID = "#1a2540"
_LINE = "#243058"

MODEL_COLORS = ["#38bdf8", "#fb923c", "#a78bfa"]
MODEL_NAMES  = ["Ridge Regression", "Gradient Boosting", "Random Forest"]


def _base_layout(title: str, height: int) -> dict:
    return dict(
        title=dict(
            text=title,
            font=dict(size=15, color="#cbd5e1", family="DM Sans, sans-serif"),
            x=0.01,
        ),
        height=height,
        paper_bgcolor=_BG,
        plot_bgcolor=_BG,
        font=dict(color="#94a3b8", family="DM Sans, sans-serif", size=12),
        hovermode="x unified",
        legend=dict(
            bgcolor="rgba(13,20,35,0.85)",
            bordercolor="#243058",
            borderwidth=1,
            font=dict(size=11),
        ),
        margin=dict(l=10, r=10, t=48, b=10),
    )


def _axis(title: str = ""):
    return dict(
        title=dict(text=title, font=dict(size=11, color="#64748b")),
        gridcolor=_GRID, linecolor=_LINE, zerolinecolor=_LINE,
        tickfont=dict(size=10),
    )


# ══════════════════════════════════════════════════════════════════════════════
# 1. Price + Indicators chart (3-row subplot)
# ══════════════════════════════════════════════════════════════════════════════

def chart_price(df: pd.DataFrame, stock_name: str) -> str:
    """Candlestick OHLC + SMA/EMA/Bollinger Bands | Volume | RSI."""
    price_col = "adj_close" if "adj_close" in df.columns else "close"
    w = df.copy()

    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        row_heights=[0.58, 0.22, 0.20],
        vertical_spacing=0.025,
        subplot_titles=("Price · SMA 20/50 · EMA 20 · Bollinger Bands", "Volume", "RSI (14)"),
    )

    dates = w["date"]

    # ── Row 1: Candlestick ────────────────────────────────────────────────
    if all(c in w.columns for c in ["open", "high", "low", "close"]):
        fig.add_trace(go.Candlestick(
            x=dates, open=w["open"], high=w["high"], low=w["low"], close=w[price_col],
            name="OHLC",
            increasing_fillcolor="#22c55e", increasing_line_color="#22c55e",
            decreasing_fillcolor="#ef4444", decreasing_line_color="#ef4444",
            line=dict(width=1),
        ), row=1, col=1)
    else:
        fig.add_trace(go.Scatter(
            x=dates, y=w[price_col], name="Price",
            line=dict(color="#38bdf8", width=2),
        ), row=1, col=1)

    # Moving averages
    if "sma_20" in w.columns:
        fig.add_trace(go.Scatter(x=dates, y=w["sma_20"], name="SMA 20",
            line=dict(color="#fb923c", width=1.5)), row=1, col=1)
    if "sma_50" in w.columns:
        fig.add_trace(go.Scatter(x=dates, y=w["sma_50"], name="SMA 50",
            line=dict(color="#a78bfa", width=1.5)), row=1, col=1)
    if "ema_20" in w.columns:
        fig.add_trace(go.Scatter(x=dates, y=w["ema_20"], name="EMA 20",
            line=dict(color="#f472b6", width=1.5, dash="dot")), row=1, col=1)

    # Bollinger Bands
    if "bb_upper" in w.columns:
        fig.add_trace(go.Scatter(x=dates, y=w["bb_upper"], name="BB Upper",
            line=dict(color="#475569", dash="dot", width=1)), row=1, col=1)
        fig.add_trace(go.Scatter(x=dates, y=w["bb_lower"], name="BB Lower",
            line=dict(color="#475569", dash="dot", width=1),
            fill="tonexty", fillcolor="rgba(71,85,105,0.07)"), row=1, col=1)

    # ── Row 2: Volume ──────────────────────────────────────────────────────
    if "volume" in w.columns:
        is_up = w[price_col] >= w[price_col].shift(1)
        colors = np.where(is_up, "rgba(34,197,94,0.4)", "rgba(239,68,68,0.4)")
        fig.add_trace(go.Bar(x=dates, y=w["volume"], name="Volume",
            marker_color=colors.tolist()), row=2, col=1)

    # ── Row 3: RSI ────────────────────────────────────────────────────────
    if "rsi" in w.columns:
        fig.add_trace(go.Scatter(x=dates, y=w["rsi"], name="RSI",
            line=dict(color="#f472b6", width=1.5)), row=3, col=1)
        fig.add_hline(y=70, line_dash="dash", line_color="#ef4444", line_width=1, row=3, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="#22c55e", line_width=1, row=3, col=1)
        fig.add_hrect(y0=70, y1=100, fillcolor="rgba(239,68,68,0.06)", row=3, col=1)
        fig.add_hrect(y0=0,  y1=30,  fillcolor="rgba(34,197,94,0.06)",  row=3, col=1)
        fig.update_yaxes(range=[0, 100], row=3, col=1)

    layout = _base_layout(f"📈  {stock_name} — Technical Analysis", 860)
    fig.update_layout(**layout, showlegend=True)
    for r in range(1, 4):
        fig.update_xaxes(gridcolor=_GRID, linecolor=_LINE, row=r, col=1, showgrid=True)
        fig.update_yaxes(gridcolor=_GRID, linecolor=_LINE, row=r, col=1, showgrid=True)
    fig.update_xaxes(rangeslider_visible=False, row=1, col=1)

    return fig.to_json()


# ══════════════════════════════════════════════════════════════════════════════
# 2. Model performance comparison
# ══════════════════════════════════════════════════════════════════════════════

def chart_performance(perf_df: pd.DataFrame) -> str:
    """4-panel bar chart: RMSE, MAE, R², CV-RMSE per model."""
    models  = perf_df.index.tolist()
    metrics = ["RMSE", "MAE", "R²", "CV-RMSE"]
    cols    = [c for c in metrics if c in perf_df.columns]

    n_cols = len(cols)
    fig = make_subplots(
        rows=1, cols=n_cols,
        horizontal_spacing=0.06,
        subplot_titles=[
            "RMSE ↓ Lower Better",
            "MAE ↓ Lower Better",
            "R² ↑ Higher Better",
            "CV-RMSE ↓ Walk-Forward",
        ][:n_cols],
    )

    palette = MODEL_COLORS + ["#22c55e", "#f59e0b"]
    colors  = [palette[i % len(palette)] for i in range(len(models))]

    for ci, metric in enumerate(cols, 1):
        vals = perf_df[metric]
        fig.add_trace(go.Bar(
            x=models, y=vals,
            name=metric,
            marker=dict(color=colors, opacity=0.9, line=dict(width=0)),
            text=[f"{v:.2f}" for v in vals],
            textposition="outside",
            textfont=dict(size=10),
        ), row=1, col=ci)
        fig.update_xaxes(tickangle=-25, gridcolor=_GRID, row=1, col=ci)
        fig.update_yaxes(gridcolor=_GRID, row=1, col=ci)

    layout = _base_layout("🤖  Model Performance Comparison", 420)
    fig.update_layout(**layout, showlegend=False)
    return fig.to_json()


# ══════════════════════════════════════════════════════════════════════════════
# 3. Predictions vs Actual (test window)
# ══════════════════════════════════════════════════════════════════════════════

def chart_overlay(df: pd.DataFrame, test_preds: dict,
                  test_start: int, name: str) -> str:
    """Actual closing price vs each model's predictions on the test window."""
    price_col = "adj_close" if "adj_close" in df.columns else "close"
    fig = go.Figure()

    # Actual price (full history)
    fig.add_trace(go.Scatter(
        x=df["date"], y=df[price_col],
        name="Actual Price",
        line=dict(color="#e2e8f0", width=2),
    ))

    # Model predictions (test window only)
    for i, (mname, preds) in enumerate(test_preds.items()):
        n     = len(preds)
        dates = df["date"].iloc[test_start:test_start + n]
        clr   = MODEL_COLORS[i % len(MODEL_COLORS)]
        fig.add_trace(go.Scatter(
            x=dates, y=preds,
            name=mname,
            line=dict(color=clr, dash="dash", width=1.8),
        ))

    # Shade the test window
    if test_start < len(df):
        fig.add_vrect(
            x0=df["date"].iloc[test_start],
            x1=df["date"].iloc[-1],
            fillcolor="rgba(56,189,248,0.04)",
            layer="below", line_width=0,
            annotation_text="Test Window",
            annotation_font_color="#38bdf8",
            annotation_font_size=10,
        )

    layout = _base_layout(f"🎯  {name} — Predictions vs Actual (Test Window)", 500)
    fig.update_layout(**layout)
    fig.update_xaxes(**_axis("Date"))
    fig.update_yaxes(**_axis("Price (₹)"))
    return fig.to_json()


# ══════════════════════════════════════════════════════════════════════════════
# 4. Target-date prediction with confidence bands
# ══════════════════════════════════════════════════════════════════════════════

def chart_target(target_pred: dict, current_price: float,
                 res_std: dict, prediction_date: str,
                 days_ahead: int) -> str:
    """
    Horizontal bar chart showing each model's prediction for the target date,
    with confidence interval (±1σ) shown as error bars.
    """
    models  = list(target_pred.keys())
    vals    = [target_pred[m] or 0 for m in models]
    errors  = [res_std.get(m, 0) * (1 + 0.15 * (days_ahead - 1)) for m in models]
    colors  = ["#22c55e" if v >= current_price else "#ef4444" for v in vals]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=models, x=vals,
        orientation="h",
        marker=dict(color=colors, opacity=0.85, line=dict(width=0)),
        error_x=dict(
            type="data", array=errors,
            color="rgba(255,255,255,0.3)", thickness=2, width=6,
        ),
        text=[f"₹{v:,.2f}" for v in vals],
        textposition="inside",
        textfont=dict(size=13, color="white"),
    ))

    # Current price vertical line
    fig.add_vline(
        x=current_price,
        line_dash="dash", line_color="#f59e0b", line_width=2,
        annotation=dict(
            text=f"Current  ₹{current_price:,.2f}",
            font=dict(color="#f59e0b", size=11),
            showarrow=False, x=current_price, yref="paper", y=1.05,
        ),
    )

    label = (f"Target {prediction_date} "
             f"({'1 trading day' if days_ahead == 1 else f'{days_ahead} trading days'} ahead)")
    layout = _base_layout(f"🔮  Prediction for {label}", 360)
    fig.update_layout(**layout)
    fig.update_xaxes(**_axis("Predicted Price (₹)"))
    fig.update_yaxes(tickfont=dict(size=12))
    return fig.to_json()


# ══════════════════════════════════════════════════════════════════════════════
# 5. Feature importance (top-10 per tree-based model)
# ══════════════════════════════════════════════════════════════════════════════

def chart_feature_importance(feat_imp: dict) -> str:
    """Horizontal bars showing top-10 feature importances for each tree model."""
    models_with_imp = [m for m in feat_imp if feat_imp[m]]
    if not models_with_imp:
        return go.Figure().to_json()

    n = len(models_with_imp)
    from plotly.subplots import make_subplots as _msp
    fig = _msp(rows=1, cols=n, horizontal_spacing=0.08,
               subplot_titles=[f"{m} — Top Features" for m in models_with_imp])

    for ci, mname in enumerate(models_with_imp, 1):
        imp = feat_imp[mname]
        feats = list(imp.keys())[::-1]
        vals  = [imp[f] for f in feats]
        clr   = MODEL_COLORS[(ci - 1) % len(MODEL_COLORS)]
        fig.add_trace(go.Bar(
            y=feats, x=vals, orientation="h",
            marker=dict(color=clr, opacity=0.85, line=dict(width=0)),
            text=[f"{v:.3f}" for v in vals], textposition="outside",
            textfont=dict(size=9),
        ), row=1, col=ci)
        fig.update_xaxes(gridcolor=_GRID, row=1, col=ci)
        fig.update_yaxes(gridcolor=_GRID, row=1, col=ci, tickfont=dict(size=9))

    layout = _base_layout("⚙️  Feature Importance (Tree-Based Models)", max(340, 80 * 10))
    fig.update_layout(**layout, showlegend=False)
    return fig.to_json()
