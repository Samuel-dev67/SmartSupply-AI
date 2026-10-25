"""SmartSupply AI — Streamlit entry point. UI + routing only; no training happens here."""
import streamlit as st

from ui import components as UI, state, theme
from ui.pages import delivery, inventory, overview, performance

st.set_page_config(page_title="SmartSupply AI", page_icon="📦", layout="wide")
theme.inject()

PAGES = {
    "📊  Overview": "Overview",
    "📦  Inventory Risk": "Inventory Risk",
    "🚚  Delivery Risk": "Delivery Risk",
    "🧪  Model Performance": "Model Performance",
}

with st.sidebar:
    st.markdown('<div class="brand">📦 SmartSupply AI</div>'
                '<div class="brand-sub">Supply Chain Intelligence</div>', unsafe_allow_html=True)
    choice = st.radio("Navigation", list(PAGES), label_visibility="collapsed")
    st.markdown('<div class="phase-chip"><b>PHASE 1</b><br>SYNTHETIC ML PROTOTYPE</div>',
                unsafe_allow_html=True)

art = state.artifacts()
data = state.scored_data()
page = PAGES[choice]

if art is None:
    UI.page_header("SmartSupply AI", "ML-based supply chain risk intelligence")
    UI.unavailable("model")
elif data is None:
    UI.page_header("SmartSupply AI", "ML-based supply chain risk intelligence")
    UI.unavailable("data")
else:
    inv, dlv = data
    if page == "Overview":
        overview.render(inv, dlv, ready=True)
    elif page == "Inventory Risk":
        inventory.render(inv, art)
    elif page == "Delivery Risk":
        delivery.render(dlv, art)
    else:
        performance.render(art)
