"""Reusable UI components. HTML is built from numeric/model values only, never raw user text."""
import html

import pandas as pd
import streamlit as st


def page_header(title: str, subtitle: str, status: list[tuple[str, bool]] | None = None) -> None:
    st.markdown(f'<div class="page-title">{html.escape(title)}</div>'
                f'<div class="page-sub">{html.escape(subtitle)}</div>', unsafe_allow_html=True)
    if status:
        pills = "".join(f'<span class="pill{" ok" if ok else ""}">{html.escape(t)}</span>'
                        for t, ok in status)
        st.markdown(f'<div class="status-row">{pills}</div>', unsafe_allow_html=True)


def section_header(title: str, caption: str | None = None) -> None:
    st.markdown(f'<div class="section-title">{html.escape(title)}</div>', unsafe_allow_html=True)
    if caption:
        st.markdown(f'<div class="section-cap">{html.escape(caption)}</div>', unsafe_allow_html=True)


def synthetic_banner() -> None:
    st.markdown(
        '<div class="synth-banner"><b>SYNTHETIC DATASET</b>&nbsp;&nbsp;Predictions and metrics shown '
        'here are generated from simulated data and rule-based labels for academic demonstration.</div>',
        unsafe_allow_html=True)


def kpi_card(label: str, value: str, caption: str = "", high: bool = False) -> None:
    cls = "kpi-value high" if high else "kpi-value"
    st.markdown(f'<div class="kpi"><div class="kpi-label">{html.escape(label)}</div>'
                f'<div class="{cls}">{html.escape(value)}</div>'
                f'<div class="kpi-cap">{html.escape(caption)}</div></div>', unsafe_allow_html=True)


def kpi_row(items: list[tuple]) -> None:
    for col, item in zip(st.columns(len(items)), items):
        with col:
            kpi_card(*item)


def risk_badge(pred: int) -> str:
    return '<span class="badge high">HIGH</span>' if pred == 1 else '<span class="badge low">LOW</span>'


def high_risk_table(df: pd.DataFrame, columns: list[tuple[str, str, str]]) -> None:
    """columns: (dataframe column, header label, format-kind) where kind is id|int|float|km|text|risk."""
    if df.empty:
        st.info("**No Matching Records** — No records match the selected filters.")
        return
    head = "".join(f'<th class="{"num" if k in ("int","float","km") else ""}">{html.escape(h)}</th>'
                   for _, h, k in columns)
    rows = []
    for _, r in df.iterrows():
        tds = []
        for col, _, kind in columns:
            v = r[col]
            if kind == "risk":
                tds.append(f"<td>{risk_badge(int(v))}</td>")
            elif kind == "id":
                tds.append(f'<td class="id">{html.escape(str(v))}</td>')
            elif kind == "int":
                tds.append(f'<td class="num">{int(v):,}</td>')
            elif kind == "km":
                tds.append(f'<td class="num">{int(v):,} km</td>')
            elif kind == "pct":
                tds.append(f'<td class="num">{float(v) * 100:.0f}%</td>')
            elif kind == "float":
                tds.append(f'<td class="num">{float(v):.2f}</td>')
            else:
                tds.append(f"<td>{html.escape(str(v))}</td>")
        rows.append("<tr>" + "".join(tds) + "</tr>")
    st.markdown(f'<div class="tbl-wrap"><table class="tbl"><thead><tr>{head}</tr></thead>'
                f'<tbody>{"".join(rows)}</tbody></table></div>', unsafe_allow_html=True)


def prediction_result(pred: int, prob: float, noun: str) -> None:
    cls, label = ("high", "HIGH RISK") if pred == 1 else ("low", "LOW RISK")
    verdict = "high" if pred == 1 else "low"
    st.markdown(
        f'<div class="result {cls}"><div class="result-head">{label}</div>'
        f'<div class="result-meta">Model prediction: <b>{pred}</b><br>'
        f'Model probability (class HIGH): <b>{prob * 100:.0f}%</b><br>'
        f'The Random Forest classifies this {noun} as {verdict} risk.</div>'
        f'<div class="note">Model probability is the Random Forest\'s output on synthetic data, '
        f'not a validated real-world likelihood.</div></div>', unsafe_allow_html=True)


def label_conditions(conds: list[tuple[str, bool]]) -> None:
    lines = "".join(
        f'<div><span class="{"on" if on else "off"}">{"✓" if on else "○"}</span>&nbsp; '
        f'{html.escape(t)}{"" if on else " — not triggered"}</div>' for t, on in conds)
    st.markdown(
        f'<div class="card" style="margin-top:12px"><div class="card-title">Synthetic Label Conditions</div>'
        f'<div class="cond">{lines}</div>'
        f'<div class="note">These are the synthetic dataset\'s label-generation rules, '
        f'not explanations produced by the Random Forest.</div></div>', unsafe_allow_html=True)


def metric_card(label: str, value: str) -> None:
    kpi_card(label, value, "synthetic held-out test")


def model_card(title: str) -> None:
    st.markdown(f'<div class="card"><div class="card-title">{html.escape(title)}</div>'
                '<div class="model-spec">Random Forest<br>100 estimators<br>'
                '80/20 train-test split<br>Random state: 42</div></div>', unsafe_allow_html=True)


def unavailable(kind: str) -> None:
    if kind == "model":
        st.error("**Model Not Available** — Train the model before using prediction features: "
                 "`python -m src.train_models`")
    else:
        st.error("**Synthetic Dataset Unavailable** — Generate or load the dataset before opening "
                 "this view: `python -m src.train_models --regenerate`")


def plot(fig) -> None:
    """Full-width Plotly chart."""
    st.plotly_chart(fig, use_container_width=True)
