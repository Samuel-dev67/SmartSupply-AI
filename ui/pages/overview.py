import streamlit as st

from ui import charts, components as UI

INV_COLS = [("record_id", "Record", "id"), ("current_stock", "Stock", "int"),
            ("daily_demand", "Demand", "int"), ("supplier_lead_time", "Lead Time", "int"),
            ("previous_stockouts", "Previous Stockouts", "int"),
            ("model_probability", "Model Prob.", "pct"), ("predicted_risk", "Risk", "risk")]
DEL_COLS = [("record_id", "Record", "id"), ("distance_km", "Distance", "km"),
            ("processing_time", "Processing", "int"), ("shipping_method", "Shipping", "text"),
            ("warehouse_delay_rate", "Delay Rate", "float"),
            ("model_probability", "Model Prob.", "pct"), ("predicted_risk", "Risk", "risk")]


def _top(df, n=8):
    hi = df[df["predicted_risk"] == 1]
    return hi.sort_values(["model_probability", "record_id"], ascending=[False, True]).head(n)


def render(inv, dlv, ready: bool) -> None:
    UI.page_header("Supply Chain Command Center", "ML-powered inventory and delivery risk intelligence",
                   [("● Models Ready" if ready else "● Models Not Found", ready), ("Synthetic Dataset", False)])
    UI.synthetic_banner()

    n_inv_hi, n_del_hi = int((inv.predicted_risk == 1).sum()), int((dlv.predicted_risk == 1).sum())
    UI.kpi_row([
        ("Inventory Records", f"{len(inv):,}", "Synthetic inventory records"),
        ("Inventory High Risk", f"{n_inv_hi:,}", "Records classified HIGH", True),
        ("Delivery Records", f"{len(dlv):,}", "Synthetic delivery records"),
        ("Delivery High Risk", f"{n_del_hi:,}", "Records classified HIGH", True),
    ])

    UI.section_header("Risk Summary", "Binary Random Forest predictions: LOW (0) or HIGH (1). "
                      "Scored on the full synthetic dataset, which includes training records.")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="card-title">Inventory Risk Distribution</div>', unsafe_allow_html=True)
        UI.plot(charts.risk_distribution(inv.predicted_risk))
        st.caption(f"{n_inv_hi:,} high-risk inventory records")
    with c2:
        st.markdown('<div class="card-title">Delivery Risk Distribution</div>', unsafe_allow_html=True)
        UI.plot(charts.risk_distribution(dlv.predicted_risk))
        st.caption(f"{n_del_hi:,} high-risk delivery records")

    UI.section_header("Priority Attention",
                      "Highest model probability among HIGH-classified records (ties ordered by record ID). "
                      "Record IDs are display-only identifiers.")
    t1, t2 = st.tabs(["Inventory", "Delivery"])
    with t1:
        UI.high_risk_table(_top(inv), INV_COLS)
    with t2:
        UI.high_risk_table(_top(dlv), DEL_COLS)
