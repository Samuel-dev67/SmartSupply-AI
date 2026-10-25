import streamlit as st

from src import config as C
from src.evaluation import feature_importance
from ui import charts, components as UI


def render(art) -> None:
    UI.page_header("Model Performance", "Random Forest evaluation on synthetic held-out test data")
    UI.synthetic_banner()

    c1, c2 = st.columns(2)
    with c1:
        UI.model_card("Inventory Model")
    with c2:
        UI.model_card("Delivery Model")

    sel1, sel2, _ = st.columns([1, 1, 2])
    dataset = sel1.selectbox("Dataset", ["Inventory", "Delivery"])
    sel2.text_input("Model", "Random Forest", disabled=True, help="Only Random Forest is implemented in Phase 1.")
    key = dataset.lower()
    m = art.metrics[key]
    model = art.inventory_model if key == "inventory" else art.delivery_model
    feats = C.INVENTORY_FEATURES if key == "inventory" else C.DELIVERY_FEATURES

    UI.section_header(f"{dataset} Metrics", f"Computed on {m['n_test']} held-out synthetic test records "
                      "(positive class = HIGH).")
    cols = st.columns(4)
    for col, (lab, k) in zip(cols, [("Accuracy", "accuracy"), ("Precision", "precision"),
                                    ("Recall", "recall"), ("F1-score", "f1")]):
        with col:
            UI.metric_card(lab, f"{m[k]:.3f}")
    st.markdown('<div class="note">High performance is expected because the target labels are generated '
                'from explicit synthetic rules. These metrics do not represent real-world model '
                'performance.</div>', unsafe_allow_html=True)

    left, right = st.columns(2)
    with left:
        UI.section_header("Classification Report")
        st.code(m["classification_report_text"], language=None)
        UI.section_header("Confusion Matrix")
        UI.plot(charts.confusion_matrix(m["confusion_matrix"]))
    with right:
        UI.section_header("Random Forest Feature Importance")
        UI.plot(charts.feature_importance(feature_importance(model, feats)))
        st.caption("Importance scores are impurity-based values from model.feature_importances_. "
                   "They describe the fitted forest on synthetic data, not real-world drivers of risk.")
        UI.section_header("Pipeline")
        st.markdown(
            '<div class="card model-spec">SYNTHETIC DATA<br>↓<br>RULE-BASED TARGET<br>↓<br>'
            'TRAIN / TEST SPLIT<br>↓<br>RANDOM FOREST<br>↓<br>CLASSIFICATION<br>↓<br>'
            'METRICS + RISK</div>', unsafe_allow_html=True)
    st.markdown('<div class="note">Only Random Forest is implemented in this prototype; no other '
                'model comparisons are shown.</div>', unsafe_allow_html=True)
