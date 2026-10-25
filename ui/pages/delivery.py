import streamlit as st

from src import config as C, predict as P
from ui import charts, components as UI

# Columns shown in the high-risk table
_TABLE_COLS = [
    ("record_id",             "Record",         "id"),
    ("distance_km",           "Distance",       "km"),
    ("processing_time",       "Processing",     "int"),
    ("order_value",           "Order Value",    "int"),
    ("shipping_method",       "Shipping",       "text"),
    ("warehouse_delay_rate",  "Delay Rate",     "float"),
    ("model_probability",     "Model Prob.",    "pct"),
    ("predicted_risk",        "Risk",           "risk"),
]


def _filters(df):
    st.markdown('<div class="card-title">Filters</div>', unsafe_allow_html=True)
    c = st.columns(5)
    risk = c[0].multiselect("Risk", ["LOW", "HIGH"], default=["LOW", "HIGH"], key="del_risk")
    ship = c[1].multiselect("Shipping method", C.SHIPPING_METHODS, default=C.SHIPPING_METHODS, key="del_ship")
    d_lo, d_hi = int(df.distance_km.min()), int(df.distance_km.max())
    p_lo, p_hi = int(df.processing_time.min()), int(df.processing_time.max())
    dist = c[2].slider("Distance (km)", d_lo, d_hi, (d_lo, d_hi), key="del_dist")
    proc = c[3].slider("Processing time", p_lo, p_hi, (p_lo, p_hi), key="del_proc")
    rate = c[4].slider("Warehouse delay rate", 0.0, 1.0, (0.0, 1.0), step=0.01, key="del_rate")
    m = df["predicted_risk"].isin([1 if r == "HIGH" else 0 for r in risk])
    m &= df["shipping_method"].isin(ship)
    m &= df["distance_km"].between(*dist) & df["processing_time"].between(*proc)
    m &= df["warehouse_delay_rate"].between(*rate)
    return df[m]


def _form(art) -> None:
    UI.section_header("Predict Delivery Risk")
    left, right = st.columns([1, 1])
    with left:
        with st.form("del_form"):
            a, b = st.columns(2)
            # Integer inputs for integer-valued features; float only for delay rate
            v = {
                "distance_km":          int(a.number_input("Distance (km)",               value=300,  step=10,  min_value=0,  format="%d")),
                "processing_time":      int(b.number_input("Processing time",              value=5,    step=1,   min_value=0,  format="%d")),
                "order_value":          int(a.number_input("Order value ($/₹)",  value=5000, step=100, min_value=0,  format="%d")),
                "warehouse_delay_rate":     b.number_input("Warehouse delay rate (0–1)",   value=0.30, step=0.05, min_value=0.0, max_value=1.0, format="%.2f"),
                "shipping_method":      a.selectbox("Shipping method", C.SHIPPING_METHODS),
            }
            go = st.form_submit_button("Analyze Delivery Risk")
    with right:
        if not go:
            st.markdown('<div class="card"><div class="card-title">Result</div>'
                        '<div class="section-cap">Enter values and run the analysis.</div></div>',
                        unsafe_allow_html=True)
            return
        errors = P.validate_delivery(v)
        if errors:
            st.error("**Invalid Input** — Please check the highlighted fields.")
            for k, msg in errors.items():
                st.markdown(f"- **{k.replace('_', ' ').capitalize()}**: {msg}")
            return
        res = P.predict_delivery(art, v)
        UI.prediction_result(res["prediction"], res["probability"], "delivery record")
        UI.label_conditions(P.delivery_conditions(v))


def render(dlv, art) -> None:
    UI.page_header("Delivery Risk Intelligence",
                   "Identify synthetic orders classified as delivery-delay risk.")
    UI.synthetic_banner()
    flt = _filters(dlv)
    hi = int((flt.predicted_risk == 1).sum())
    UI.kpi_row([
        ("Total Delivery Records",  f"{len(flt):,}",                                          "Matching current filters"),
        ("High Risk",               f"{hi:,}",                                                 "Records classified HIGH", True),
        ("Average Distance",        f"{flt.distance_km.mean():.0f} km" if len(flt) else "—",  "Kilometres"),
        ("Average Processing Time", f"{flt.processing_time.mean():.1f}"  if len(flt) else "—", "Processing units"),
    ])

    if flt.empty:
        st.info("**No Matching Records** — No records match the selected filters.")
    else:
        c1, c2 = st.columns([1, 2])
        with c1:
            UI.section_header("Risk Distribution")
            UI.plot(charts.risk_distribution(flt.predicted_risk))
        with c2:
            UI.section_header("Distance vs Processing Time", "Colored by model-predicted risk.")
            UI.plot(charts.distance_vs_processing(flt))
            st.caption("Dashed lines: synthetic label rule reference (500 km, processing time 10). "
                       "They are the dataset's generation rules, not learned decision boundaries.")

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
