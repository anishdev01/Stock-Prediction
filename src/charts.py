# ══════════════════════════════════════════════════════════════════════════════
#  TASK 5 — CHARTS (UPGRADED)
#  Interactive Plotly charts with modern dark theme
#  Indian Stock Predictor · Alpha Five Team · Brainware University
# ══════════════════════════════════════════════════════════════════════════════

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ── Modern Dark Theme ──────────────────────────────────────────────────────

_BG = "rgba(0,0,0,0)"
_GRID = "#1e2f4a"
_LINE = "#2a3f5f"

MODEL_COLORS = {
    "Linear Regression": "#38bdf8",  # Cyan
    "Ridge Regression": "#fb923c",    # Orange
    "LSTM": "#a78bfa",                # Purple
}


def _base_layout(title: str, height: int) -> dict:
    return dict(
        title=dict(
            text=title,
            font=dict(size=16, color="#e8eef6", family="Space Grotesk, sans-serif", weight=700),
            x=0.01,
        ),
        height=height,
        paper_bgcolor=_BG,
        plot_bgcolor=_BG,
        font=dict(color="#94a3b8", family="Space Grotesk, sans-serif", size=12),
        hovermode="x unified",
        legend=dict(
            bgcolor="rgba(13,20,35,0.9)",
            bordercolor="#2a3f5f",
            borderwidth=1,
            font=dict(size=11),
        ),
        margin=dict(l=15, r=15, t=55, b=15),
    )


def _axis(title: str = ""):
    return dict(
        title=dict(text=title, font=dict(size=12, color="#64748b")),
        gridcolor=_GRID,
        linecolor=_LINE,
        zerolinecolor=_LINE,
        tickfont=dict(size=10),
    )


# ══════════════════════════════════════════════════════════════════════════════
# 1. Price Chart with Technical Indicators
# ══════════════════════════════════════════════════════════════════════════════

def chart_price(df: pd.DataFrame, stock_name: str) -> str:
    """Multi-panel chart: Price + SMA + Bollinger / Volume / RSI"""
    price_col = "adj_close" if "adj_close" in df.columns else "close"
    w = df.copy()

    # Calculate RSI if missing
    if "rsi" not in w.columns:
        d = w[price_col].diff()
        g = d.clip(lower=0).rolling(14, min_periods=5).mean()
        l = (-d.clip(upper=0)).rolling(14, min_periods=5).mean()
        w["rsi"] = (100 - 100 / (1 + g / l.replace(0, np.nan))).fillna(50)

    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        row_heights=[0.60, 0.20, 0.20],
        vertical_spacing=0.025,
        subplot_titles=("📈 Price + Moving Averages + Bollinger Bands", "📊 Volume", "📉 RSI (14)"),
    )

    dates = w["date"]
    p = w[price_col]

    # Row 1: Candlestick or Line
    if all(c in w.columns for c in ["open", "high", "low", "close"]):
        fig.add_trace(go.Candlestick(
            x=dates, open=w["open"], high=w["high"], low=w["low"], close=w[price_col],
            name="OHLC",
            increasing_fillcolor="#22c55e", increasing_line_color="#22c55e",
            decreasing_fillcolor="#ef4444", decreasing_line_color="#ef4444",
            line=dict(width=1.2),
        ), row=1, col=1)
    else:
        fig.add_trace(go.Scatter(
            x=dates, y=p, name="Price",
            line=dict(color="#38bdf8", width=2.5),
        ), row=1, col=1)

    # Moving Averages
    if "sma_20" in w.columns:
        fig.add_trace(go.Scatter(
            x=dates, y=w["sma_20"], name="SMA 20",
            line=dict(color="#fb923c", width=1.8),
        ), row=1, col=1)
    if "sma_50" in w.columns:
        fig.add_trace(go.Scatter(
            x=dates, y=w["sma_50"], name="SMA 50",
            line=dict(color="#a78bfa", width=1.8),
        ), row=1, col=1)

    # Bollinger Bands
    if "bb_upper" in w.columns:
        fig.add_trace(go.Scatter(
            x=dates, y=w["bb_upper"], name="BB Upper",
            line=dict(color="#475569", dash="dot", width=1.2),
        ), row=1, col=1)
        fig.add_trace(go.Scatter(
            x=dates, y=w["bb_lower"], name="BB Lower",
            line=dict(color="#475569", dash="dot", width=1.2),
            fill="tonexty", fillcolor="rgba(71,85,105,0.08)",
        ), row=1, col=1)

    # Row 2: Volume
    if "volume" in w.columns:
        is_up = w[price_col] >= w[price_col].shift(1)
        colors = np.where(is_up, "rgba(34,197,94,0.5)", "rgba(239,68,68,0.5)")
        fig.add_trace(go.Bar(
            x=dates, y=w["volume"], name="Volume",
            marker_color=colors.tolist(),
        ), row=2, col=1)

    # Row 3: RSI
    fig.add_trace(go.Scatter(
        x=dates, y=w["rsi"], name="RSI",
        line=dict(color="#f472b6", width=2),
    ), row=3, col=1)
    
    fig.add_hline(y=70, line_dash="dash", line_color="#ef4444", line_width=1.5, row=3, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="#22c55e", line_width=1.5, row=3, col=1)
    fig.add_hrect(y0=70, y1=100, fillcolor="rgba(239,68,68,0.08)", row=3, col=1, line_width=0)
    fig.add_hrect(y0=0, y1=30, fillcolor="rgba(34,197,94,0.08)", row=3, col=1, line_width=0)
    fig.update_yaxes(range=[0, 100], row=3, col=1)

    layout = _base_layout(f"🎯 {stock_name} — Technical Analysis Dashboard", 860)
    fig.update_layout(**layout, showlegend=True)
    
    for r in range(1, 4):
        fig.update_xaxes(gridcolor=_GRID, linecolor=_LINE, row=r, col=1, showgrid=True)
        fig.update_yaxes(gridcolor=_GRID, linecolor=_LINE, row=r, col=1, showgrid=True)
    
    fig.update_xaxes(rangeslider_visible=False, row=1, col=1)

    return fig.to_json()


# ══════════════════════════════════════════════════════════════════════════════
# 2. Model Performance Comparison
# ══════════════════════════════════════════════════════════════════════════════

def chart_performance(perf_df: pd.DataFrame) -> str:
    """3-panel bar chart: RMSE, MAE, R² per model"""
    models = perf_df.index.tolist()
    colors = [MODEL_COLORS.get(m, "#64748b") for m in models]

    fig = make_subplots(
        rows=1, cols=3,
        horizontal_spacing=0.08,
        subplot_titles=("RMSE ↓ (Lower is Better)", "MAE ↓ (Lower is Better)", "R² ↑ (Higher is Better)"),
    )

    for col, metric in enumerate(["RMSE", "MAE", "R²"], 1):
        if metric in perf_df.columns:
            vals = perf_df[metric]
            fig.add_trace(go.Bar(
                x=models, y=vals, name=metric,
                marker=dict(color=colors, opacity=0.9, line=dict(width=0)),
                text=[f"{v:.3f}" for v in vals],
                textposition="outside",
                textfont=dict(size=11, color="#e8eef6"),
            ), row=1, col=col)
            
            fig.update_xaxes(tickangle=-25, gridcolor=_GRID, linecolor=_LINE, row=1, col=col)
            fig.update_yaxes(gridcolor=_GRID, linecolor=_LINE, row=1, col=col)

    layout = _base_layout("🤖 Model Performance Comparison", 420)
    fig.update_layout(**layout, showlegend=False)
    return fig.to_json()


# ══════════════════════════════════════════════════════════════════════════════
# 3. Predictions vs Actual (Test Window)
# ══════════════════════════════════════════════════════════════════════════════

def chart_overlay(df: pd.DataFrame, test_preds: dict, test_start: int, name: str) -> str:
    """Actual price vs model predictions on test window"""
    price_col = "adj_close" if "adj_close" in df.columns else "close"
    fig = go.Figure()

    # Actual price
    fig.add_trace(go.Scatter(
        x=df["date"], y=df[price_col],
        name="Actual Price",
        line=dict(color="#e2e8f0", width=2.5),
    ))

    # Model predictions
    for mname, preds in test_preds.items():
        # Filter None values
        valid_preds = [p for p in preds if p is not None]
        if not valid_preds:
            continue
            
        n = len(valid_preds)
        dates = df["date"].iloc[test_start:test_start + n]
        color = MODEL_COLORS.get(mname, "#64748b")
        
        fig.add_trace(go.Scatter(
            x=dates, y=valid_preds,
            name=mname,
            line=dict(color=color, dash="dash", width=2),
        ))

    # Shade test window
    if test_start < len(df):
        fig.add_vrect(
            x0=df["date"].iloc[test_start],
            x1=df["date"].iloc[-1],
            fillcolor="rgba(56,189,248,0.05)",
            layer="below",
            line_width=0,
            annotation_text="Test Window",
            annotation_font_color="#38bdf8",
            annotation_font_size=11,
        )

    layout = _base_layout(f"🎯 {name} — Predictions vs Actual (Test Window)", 520)
    fig.update_layout(**layout)
    fig.update_xaxes(**_axis("Date"))
    fig.update_yaxes(**_axis("Price (₹)"))
    return fig.to_json()


# ══════════════════════════════════════════════════════════════════════════════
# 4. Next-Day Prediction Chart
# ══════════════════════════════════════════════════════════════════════════════

def chart_next(next_pred: dict, current_price: float) -> str:
    """Horizontal bar chart of next-day predictions"""
    models = [m for m in next_pred.keys() if next_pred[m] is not None]
    vals = [next_pred[m] for m in models]
    colors = [MODEL_COLORS.get(m, "#64748b") for m in models]
    bar_colors = ["#22c55e" if v > current_price else "#ef4444" for v in vals]

    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=models, x=vals,
        orientation="h",
        marker=dict(color=bar_colors, opacity=0.85, line=dict(width=0)),
        text=[f"₹{v:,.2f}" for v in vals],
        textposition="inside",
        textfont=dict(size=13, color="white", weight=600),
    ))

    # Current price line
    fig.add_vline(
        x=current_price,
        line_dash="dash",
        line_color="#f59e0b",
        line_width=2.5,
        annotation=dict(
            text=f"Current ₹{current_price:,.2f}",
            font=dict(color="#f59e0b", size=12, weight=600),
            showarrow=False,
            x=current_price,
            yref="paper",
            y=1.05,
        ),
    )

    layout = _base_layout("🔮 Next-Day Price Predictions", 350)
    fig.update_layout(**layout)
    fig.update_xaxes(**_axis("Predicted Price (₹)"))
    fig.update_yaxes(tickfont=dict(size=12))
    return fig.to_json()


# ══════════════════════════════════════════════════════════════════════════════
# 5. Feature Importance Chart
# ══════════════════════════════════════════════════════════════════════════════

def chart_feature_importance(feat_imp: dict) -> str:
    """Top feature importances for each model"""
    models_with_imp = [m for m in feat_imp if feat_imp[m]]
    if not models_with_imp:
        return go.Figure().to_json()

    n = len(models_with_imp)
    fig = make_subplots(
        rows=1, cols=n,
        horizontal_spacing=0.10,
        subplot_titles=[f"{m} — Top Features" for m in models_with_imp],
    )

    for ci, mname in enumerate(models_with_imp, 1):
        imp = feat_imp[mname]
        feats = list(imp.keys())[::-1]  # Reverse for bottom-up display
        vals = [imp[f] for f in feats]
        color = MODEL_COLORS.get(mname, "#64748b")
        
        fig.add_trace(go.Bar(
            y=feats, x=vals,
            orientation="h",
            marker=dict(color=color, opacity=0.85, line=dict(width=0)),
            text=[f"{v:.3f}" for v in vals],
            textposition="outside",
            textfont=dict(size=9),
        ), row=1, col=ci)
        
        fig.update_xaxes(gridcolor=_GRID, linecolor=_LINE, row=1, col=ci)
        fig.update_yaxes(gridcolor=_GRID, linecolor=_LINE, row=1, col=ci, tickfont=dict(size=9))

    layout = _base_layout("⚙️ Feature Importance Analysis", max(380, 60 * len(feats)))
    fig.update_layout(**layout, showlegend=False)
    return fig.to_json()
