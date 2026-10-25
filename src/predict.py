"""Inference layer: loads saved artifacts, validates input, predicts. No Streamlit, no training."""
import json
from dataclasses import dataclass

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split

from . import config as C


class ArtifactsMissing(Exception):
    """Raised when required model/data files are not on disk."""


@dataclass
class Artifacts:
    inventory_model: object
    delivery_model: object
    shipping_encoder: object
    metrics: dict


def load_artifacts() -> Artifacts:
    needed = [C.INVENTORY_MODEL, C.DELIVERY_MODEL, C.SHIPPING_ENCODER, C.METRICS_JSON]
    if any(not p.exists() for p in needed):
        raise ArtifactsMissing("Model artifacts not found.")
    return Artifacts(
        inventory_model=joblib.load(C.INVENTORY_MODEL),
        delivery_model=joblib.load(C.DELIVERY_MODEL),
        shipping_encoder=joblib.load(C.SHIPPING_ENCODER),
        metrics=json.loads(C.METRICS_JSON.read_text()),
    )


def load_datasets() -> tuple[pd.DataFrame, pd.DataFrame]:
    if not (C.INVENTORY_CSV.exists() and C.DELIVERY_CSV.exists()):
        raise ArtifactsMissing("Synthetic dataset not found.")
    return pd.read_csv(C.INVENTORY_CSV), pd.read_csv(C.DELIVERY_CSV)


# ---------------------------------------------------------------- validation
def validate_inventory(v: dict) -> dict:
    return {k: "Must be 0 or greater" for k in C.INVENTORY_FEATURES
            if v.get(k) is None or v[k] < 0}


def validate_delivery(v: dict) -> dict:
    errors = {}
    for k in ("distance_km", "processing_time", "order_value"):
        if v.get(k) is None or v[k] < 0:
            errors[k] = "Must be 0 or greater"
    rate = v.get("warehouse_delay_rate")
    if rate is None or not 0 <= rate <= 1:
        errors["warehouse_delay_rate"] = "Must be between 0 and 1"
    if v.get("shipping_method") not in C.SHIPPING_METHODS:
        errors["shipping_method"] = "Choose Standard or Express"
    return errors


# ---------------------------------------------------------------- prediction
def _result(model, X: pd.DataFrame) -> dict:
    pred = int(model.predict(X)[0])
    proba = model.predict_proba(X)[0]
    classes = list(model.classes_)
    p_high = float(proba[classes.index(1)]) if 1 in classes else 0.0
    return {"prediction": pred, "probability": p_high}


def predict_inventory(art: Artifacts, v: dict) -> dict:
    X = pd.DataFrame([[v[k] for k in C.INVENTORY_FEATURES]], columns=C.INVENTORY_FEATURES)
    return _result(art.inventory_model, X)


def predict_delivery(art: Artifacts, v: dict) -> dict:
    row = dict(v)
    row["shipping_method"] = int(art.shipping_encoder.transform([v["shipping_method"]])[0])
    X = pd.DataFrame([[row[k] for k in C.DELIVERY_FEATURES]], columns=C.DELIVERY_FEATURES)
    return _result(art.delivery_model, X)


# ----------------------------------------------- synthetic label-rule indicators
def inventory_conditions(v: dict) -> list[tuple[str, bool]]:
    """Dataset label-generation rules, NOT Random Forest explanations."""
    return [
        ("Stock below 3× daily demand", v["current_stock"] < v["daily_demand"] * 3),
        ("Supplier lead time above 10 days", v["supplier_lead_time"] > 10),
        ("Previous stockouts at or above 3", v["previous_stockouts"] >= 3),
    ]


def delivery_conditions(v: dict) -> list[tuple[str, bool]]:
    return [
        ("Distance above 500 km", v["distance_km"] > 500),
        ("Processing time above 10", v["processing_time"] > 10),
        ("Warehouse delay rate above 0.6", v["warehouse_delay_rate"] > 0.6),
    ]


# ------------------------------------------------------- dataset-level scoring
def _split_flags(n: int) -> pd.Series:
    idx_train, idx_test = train_test_split(
        range(n), test_size=C.TEST_SIZE, random_state=C.SEED
    )
    s = pd.Series("train", index=range(n))
    s.loc[idx_test] = "test"
    return s


def score_inventory(art: Artifacts, df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    X = out[C.INVENTORY_FEATURES]
    out["record_id"] = [f"INV-{i + 1:04d}" for i in range(len(out))]  # display-only
    out["predicted_risk"] = art.inventory_model.predict(X)
    out["model_probability"] = art.inventory_model.predict_proba(X)[:, 1]
    out["split"] = _split_flags(len(out)).values
    return out


def score_delivery(art: Artifacts, df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    X = out[C.DELIVERY_FEATURES].copy()
    X["shipping_method"] = art.shipping_encoder.transform(X["shipping_method"])
    out["record_id"] = [f"ORD-{i + 1:04d}" for i in range(len(out))]  # display-only
    out["predicted_risk"] = art.delivery_model.predict(X)
    out["model_probability"] = art.delivery_model.predict_proba(X)[:, 1]
    out["split"] = _split_flags(len(out)).values
    return out
