"""Design tokens + global CSS (see DESIGN.md)."""
import streamlit as st

BG, SURFACE, ELEVATED, BORDER = "#0B1120", "#111827", "#172033", "#243047"
ACCENT = "#38BDF8"
TEXT, TEXT_2, MUTED = "#F8FAFC", "#CBD5E1", "#94A3B8"
LOW, HIGH, WARN = "#22C55E", "#EF4444", "#F59E0B"

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"], .stApp {{ font-family: 'Inter', 'Plus Jakarta Sans', system-ui, sans-serif; }}
.stApp {{ background: {BG}; color: {TEXT}; }}
#MainMenu, footer, .stDeployButton {{ visibility: hidden; height: 0; }}
.block-container {{ padding: 1.6rem 2.2rem 3rem; max-width: 1400px; }}

/* sidebar */
section[data-testid="stSidebar"] {{ background: {SURFACE}; border-right: 1px solid {BORDER}; }}
section[data-testid="stSidebar"] .block-container {{ padding: 1.4rem 1rem; }}
.brand {{ font-size: 20px; font-weight: 700; color: {TEXT}; }}
.brand-sub {{ font-size: 12px; color: {MUTED}; margin: 2px 0 18px; letter-spacing: .02em; }}
.phase-chip {{ margin-top: 28px; padding: 10px 12px; border: 1px solid {BORDER}; border-radius: 10px;
  background: {ELEVATED}; font-size: 11px; letter-spacing: .08em; color: {MUTED}; line-height: 1.5; }}
.phase-chip b {{ color: {ACCENT}; }}
div[role="radiogroup"] {{ gap: 4px; }}
div[role="radiogroup"] > label {{ background: transparent; border: 1px solid transparent; border-radius: 10px;
  padding: 8px 12px; width: 100%; transition: background .12s; }}
div[role="radiogroup"] > label:hover {{ background: {ELEVATED}; }}
div[role="radiogroup"] > label:has(input:checked) {{ background: {ELEVATED}; border-color: {ACCENT}; }}
div[role="radiogroup"] > label > div:first-child {{ display: none; }}
div[role="radiogroup"] label p {{ font-size: 14px; font-weight: 500; color: {TEXT_2}; }}
div[role="radiogroup"] > label:has(input:checked) p {{ color: {ACCENT}; font-weight: 600; }}

/* headers */
.page-title {{ font-size: 30px; font-weight: 700; margin: 0; color: {TEXT}; }}
.page-sub {{ font-size: 15px; color: {MUTED}; margin: 2px 0 14px; }}
.status-row {{ display:flex; gap:10px; margin: 0 0 14px; flex-wrap: wrap; }}
.pill {{ font-size: 12px; padding: 3px 10px; border-radius: 999px; border: 1px solid {BORDER};
  background: {ELEVATED}; color: {TEXT_2}; }}
.pill.ok {{ color: {LOW}; }}
.section-title {{ font-size: 19px; font-weight: 600; margin: 22px 0 8px; color: {TEXT}; }}
.section-cap {{ font-size: 13px; color: {MUTED}; margin: -4px 0 10px; }}

/* banner */
.synth-banner {{ border: 1px solid {WARN}55; border-left: 3px solid {WARN}; background: {WARN}10;
  border-radius: 10px; padding: 10px 14px; margin: 0 0 16px; font-size: 13px; color: {TEXT_2}; }}
.synth-banner b {{ color: {WARN}; letter-spacing: .06em; font-size: 12px; }}

/* cards */
.kpi {{ background: {SURFACE}; border: 1px solid {BORDER}; border-radius: 14px; padding: 16px 18px; height: 100%; }}
.kpi-label {{ font-size: 12.5px; color: {MUTED}; font-weight: 500; }}
.kpi-value {{ font-size: 28px; font-weight: 700; color: {TEXT}; margin: 4px 0 2px; }}
.kpi-value.high {{ color: {HIGH}; }}
.kpi-cap {{ font-size: 12px; color: {MUTED}; }}
.card {{ background: {SURFACE}; border: 1px solid {BORDER}; border-radius: 14px; padding: 16px 20px; }}
.card-title {{ font-size: 14px; font-weight: 600; color: {TEXT}; margin-bottom: 6px; }}
.model-spec {{ font-size: 13px; color: {TEXT_2}; line-height: 1.7; }}

/* risk */
.badge {{ display:inline-block; font-size: 11.5px; font-weight: 700; letter-spacing: .05em;
  padding: 2px 9px; border-radius: 6px; }}
.badge.low {{ color: {LOW}; background: {LOW}1A; border: 1px solid {LOW}55; }}
.badge.high {{ color: {HIGH}; background: {HIGH}1A; border: 1px solid {HIGH}55; }}
.result {{ border-radius: 14px; padding: 16px 20px; background: {SURFACE}; border: 1px solid {BORDER}; }}
.result.high {{ border-left: 4px solid {HIGH}; }} .result.low {{ border-left: 4px solid {LOW}; }}
.result-head {{ font-size: 22px; font-weight: 700; }}
.result.high .result-head {{ color: {HIGH}; }} .result.low .result-head {{ color: {LOW}; }}
.result-meta {{ font-size: 13.5px; color: {TEXT_2}; margin-top: 6px; line-height: 1.6; }}
.cond {{ font-size: 13.5px; color: {TEXT_2}; line-height: 1.9; }}
.cond .on {{ color: {WARN}; font-weight: 600; }} .cond .off {{ color: {MUTED}; }}
.note {{ font-size: 12px; color: {MUTED}; margin-top: 8px; }}

/* tables */
.tbl-wrap {{ overflow-x: auto; border: 1px solid {BORDER}; border-radius: 12px; background: {SURFACE}; }}
table.tbl {{ width: 100%; border-collapse: collapse; font-size: 13.5px; }}
table.tbl th {{ text-align: left; color: {MUTED}; font-weight: 500; padding: 10px 14px; border-bottom: 1px solid {BORDER}; white-space: nowrap; }}
table.tbl td {{ padding: 9px 14px; color: {TEXT_2}; border-bottom: 1px solid {BORDER}80; white-space: nowrap; }}
table.tbl tr:last-child td {{ border-bottom: none; }}
table.tbl td.num, table.tbl th.num {{ text-align: right; font-variant-numeric: tabular-nums; }}
table.tbl td.id {{ color: {TEXT}; font-weight: 600; }}

/* inputs / buttons */
div[data-testid="stForm"] {{ background: {SURFACE}; border: 1px solid {BORDER}; border-radius: 14px; padding: 16px 20px; }}
.stButton > button, div[data-testid="stFormSubmitButton"] > button {{
  background: {ACCENT}; color: #06121F; font-weight: 600; border: none; border-radius: 9px; padding: 6px 18px; }}
.stButton > button:hover, div[data-testid="stFormSubmitButton"] > button:hover {{ background: #7DD3FC; color: #06121F; }}
div[data-testid="stTabs"] button[aria-selected="true"] {{ color: {ACCENT}; }}
</style>
"""


def inject() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
