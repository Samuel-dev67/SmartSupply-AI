"""Cached loaders so Streamlit reruns never reload from disk or retrain."""
import streamlit as st

from src import predict as P


@st.cache_resource(show_spinner=False)
def artifacts():
    try:
        return P.load_artifacts()
    except P.ArtifactsMissing:
        return None


@st.cache_data(show_spinner=False)
def scored_data():
    art = artifacts()
    if art is None:
        return None
    try:
        inv, dlv = P.load_datasets()
    except P.ArtifactsMissing:
        return None
    return P.score_inventory(art, inv), P.score_delivery(art, dlv)
