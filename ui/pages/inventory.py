import streamlit as st

from src import predict as P
from ui import charts, components as UI

# Columns shown in the high-risk table
_TABLE_COLS = [
    ("record_id",           "Record",            "id"),
    ("current_stock",       "Stock",             "int"),
    ("daily_demand",        "Demand",            "int"),
    ("supplier_lead_time",  "Lead Time (days)",  "int"),
    ("previous_stockouts",  "Stockouts",         "int"),
    ("sales_last_7_days",   "Sales 7d",          "int"),
    ("model_probability",   "Model Prob.",        "pct"),
    ("predicted_risk",      "Risk",              "risk"),
]


def _filters(df):
    st.markdown('<div class="card-title">Filters</div>', unsafe_allow_html=True)
    c = st.columns(5)
    risk = c[0].multiselect("Risk", ["LOW", "HIGH"], default=["LOW", "HIGH"], key="inv_risk")

    def rng(col, label, slot, key):
        lo, hi = int(df[col].min()), int(df[col].max())
        return slot.slider(label, lo, hi, (lo, hi), key=key)

    stock  = rng("current_stock",      "Current stock",      c[1], "inv_stock")
    demand = rng("daily_demand",        "Daily demand",       c[2], "inv_demand")
    lead   = rng("supplier_lead_time",  "Lead time (days)",  c[3], "inv_lead")
    outs   = rng("previous_stockouts",  "Prev. stockouts",   c[4], "inv_outs")

    m = df["predicted_risk"].isin([1 if r == "HIGH" else 0 for r in risk])
    for col, (lo, hi) in [("current_stock", stock), ("daily_demand", demand),
                           ("supplier_lead_time", lead), ("previous_stockouts", outs)]:
        m &= df[col].between(lo, hi)
    return df[m]


def _form(art) -> None:
    UI.section_header("Predict Inventory Risk")
    left, right = st.columns([1, 1])
    with left:
        with st.form("inv_form"):
            a, b = st.columns(2)
            # Integer inputs for integer-valued features; step=1, no decimals
            v = {
                "current_stock":      int(a.number_input("Current stock",          value=150,  step=1,   min_value=0, format="%d")),
                "daily_demand":       int(b.number_input("Daily demand",            value=10,   step=1,   min_value=0, format="%d")),
                "supplier_lead_time": int(a.number_input("Supplier lead time (days)", value=7, step=1,   min_value=0, format="%d")),
                "previous_stockouts": int(b.number_input("Previous stockouts",     value=1,    step=1,   min_value=0, format="%d")),
                "sales_last_7_days":  int(a.number_input("Sales last 7 days",      value=100,  step=1,   min_value=0, format="%d")),
            }
            go = st.form_submit_button("Analyze Inventory Risk")
    with right:
        if not go:
            st.markdown('<div class="card"><div class="card-title">Result</div>'
                        '<div class="section-cap">Enter values and run the analysis.</div></div>',
                        unsafe_allow_html=True)
            return
        errors = P.validate_inventory(v)
        if errors:
            st.error("**Invalid Input** — Please check the highlighted fields.")
            for k, msg in errors.items():
                st.markdown(f"- **{k.replace('_', ' ').capitalize()}**: {msg}")
            return
        res = P.predict_inventory(art, v)
        UI.prediction_result(res["prediction"], res["probability"], "record")
        UI.label_conditions(P.inventory_conditions(v))


def render(inv, art) -> None:
    UI.page_header("Inventory Risk Intelligence",
                   "Identify synthetic inventory records classified as stockout risk.")
    UI.synthetic_banner()
    flt = _filters(inv)
    hi = int((flt.predicted_risk == 1).sum())
    UI.kpi_row([
        ("Total Inventory Records", f"{len(flt):,}",                                  "Matching current filters"),
        ("High Risk",               f"{hi:,}",                                         "Records classified HIGH", True),
        ("Average Stock",           f"{flt.current_stock.mean():.0f}" if len(flt) else "—", "Units"),
        ("Average Daily Demand",    f"{flt.daily_demand.mean():.1f}"  if len(flt) else "—", "Units per day"),
    ])

    if flt.empty:
        st.info("**No Matching Records** — No records match the selected filters.")
    else:
        c1, c2 = st.columns([1, 2])
        with c1:
            UI.section_header("Risk Distribution")
            UI.plot(charts.risk_distribution(flt.predicted_risk))
        with c2:
            UI.section_header("Stock vs Demand", "Colored by model-predicted risk.")
            UI.plot(charts.stock_vs_demand(flt))
            st.caption("Dashed line: synthetic label rule reference (stock = 3 × daily demand). "
                       "It is the dataset's generation rule, not a learned threshold.")

        # --- High-risk records table ---
        hi_df = (
            flt[flt["predicted_risk"] == 1]
            .sort_values("model_probability", ascending=False)
            .head(100)
        )
        UI.section_header(
            "High-Risk Records",
            f"{len(hi_df):,} records classified HIGH within current filters — "
            "sorted by model probability (descending, top 100 max)."
        )
        UI.high_risk_table(hi_df, _TABLE_COLS)

    _form(art)
