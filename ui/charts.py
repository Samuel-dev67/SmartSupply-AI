"""Plotly figures: dark, restrained. Red/green only for risk states, cyan for analytic series."""
import pandas as pd
import plotly.graph_objects as go

from . import theme as T

RISK_COLOR = {0: T.LOW, 1: T.HIGH}
RISK_NAME = {0: "LOW", 1: "HIGH"}
REF_LABEL = "Synthetic label rule reference"


def _layout(fig: go.Figure, height: int = 340) -> go.Figure:
    fig.update_layout(
        height=height, margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, system-ui, sans-serif", color=T.TEXT_2, size=13),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_xaxes(gridcolor=T.BORDER, zerolinecolor=T.BORDER, linecolor=T.BORDER)
    fig.update_yaxes(gridcolor=T.BORDER, zerolinecolor=T.BORDER, linecolor=T.BORDER)
    return fig


def risk_distribution(pred: pd.Series) -> go.Figure:
    counts = pred.value_counts().reindex([0, 1], fill_value=0)
    fig = go.Figure(go.Pie(
        labels=[RISK_NAME[k] for k in counts.index], values=counts.values, hole=0.62,
        marker=dict(colors=[RISK_COLOR[k] for k in counts.index], line=dict(color=T.BG, width=2)),
        textinfo="label+value", textfont=dict(color=T.TEXT), sort=False,
    ))
    fig.update_layout(showlegend=False)
    return _layout(fig, 260)


def _risk_scatter(df, x, y, xlab, ylab, hover) -> go.Figure:
    fig = go.Figure()
    for k in (0, 1):
        d = df[df["predicted_risk"] == k]
        fig.add_trace(go.Scatter(
            x=d[x], y=d[y], mode="markers", name=RISK_NAME[k],
            marker=dict(color=RISK_COLOR[k], size=7, opacity=0.75,
                        symbol="circle" if k == 0 else "diamond"),
            customdata=d[["record_id", "model_probability"]].values,
            hovertemplate=hover,
        ))
    fig.update_xaxes(title=xlab)
    fig.update_yaxes(title=ylab)
    return fig


def stock_vs_demand(df: pd.DataFrame) -> go.Figure:
    fig = _risk_scatter(
        df, "daily_demand", "current_stock", "Daily demand", "Current stock",
        "%{customdata[0]}<br>Demand %{x}<br>Stock %{y}<br>Model prob. %{customdata[1]:.0%}<extra></extra>")
    if not df.empty:
        xmax = float(df["daily_demand"].max())
        fig.add_trace(go.Scatter(
            x=[0, xmax], y=[0, xmax * 3], mode="lines", name=f"{REF_LABEL}: stock = 3 × demand",
            line=dict(color=T.ACCENT, width=1.5, dash="dash"), hoverinfo="skip"))
    return _layout(fig, 380)


def distance_vs_processing(df: pd.DataFrame) -> go.Figure:
    fig = _risk_scatter(
        df, "distance_km", "processing_time", "Distance (km)", "Processing time",
        "%{customdata[0]}<br>%{x} km<br>Processing %{y}<br>Model prob. %{customdata[1]:.0%}<extra></extra>")
    fig.add_vline(x=500, line=dict(color=T.ACCENT, width=1.2, dash="dash"),
                  annotation_text="500 km", annotation_font_color=T.ACCENT)
    fig.add_hline(y=10, line=dict(color=T.ACCENT, width=1.2, dash="dash"),
                  annotation_text="processing = 10", annotation_font_color=T.ACCENT)
    fig.add_annotation(text=REF_LABEL, xref="paper", yref="paper", x=1, y=1.12,
                       showarrow=False, font=dict(size=11, color=T.MUTED), xanchor="right")
    return _layout(fig, 380)


def confusion_matrix(cm: list[list[int]]) -> go.Figure:
    labels = ["Class 0 / Low", "Class 1 / High"]
    fig = go.Figure(go.Heatmap(
        z=cm, x=labels, y=labels, text=cm, texttemplate="%{text}", textfont=dict(size=22, color=T.TEXT),
        colorscale=[[0, T.ELEVATED], [1, "#0EA5E9"]], showscale=False,
        hovertemplate="Actual %{y}<br>Predicted %{x}<br>Count %{z}<extra></extra>"))
    fig.update_xaxes(title="Predicted", side="bottom")
    fig.update_yaxes(title="Actual", autorange="reversed")
    return _layout(fig, 340)


def feature_importance(fi: pd.DataFrame) -> go.Figure:
    fi = fi.sort_values("importance", ascending=True)  # largest on top in a horizontal bar
    fig = go.Figure(go.Bar(
        x=fi["importance"], y=fi["feature"], orientation="h", marker_color=T.ACCENT,
        text=[f"{v:.3f}" for v in fi["importance"]], textposition="outside",
        textfont=dict(color=T.TEXT_2)))
    fig.update_xaxes(title="Importance (model.feature_importances_)")
    return _layout(fig, 320)
