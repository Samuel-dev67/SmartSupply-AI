"""Train once, save artifacts. Run: python -m src.train_models [--regenerate]

Uses a single continuous random stream for data generation (seed set once
before all generation calls). Never imported by the Streamlit UI at runtime,
so widget reruns never retrain.
"""
import argparse
import json

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from . import config as C
from .data_generator import generate_both


def _split(X, y):
    return train_test_split(X, y, test_size=C.TEST_SIZE, random_state=C.SEED)


def _new_model() -> RandomForestClassifier:
    return RandomForestClassifier(n_estimators=C.N_ESTIMATORS, random_state=C.SEED)


def train_inventory(df):
    X, y = df[C.INVENTORY_FEATURES], df["inventory_risk"]
    X_train, X_test, y_train, y_test = _split(X, y)
    model = _new_model().fit(X_train, y_train)
    from .evaluation import evaluate
    return model, evaluate(y_test, model.predict(X_test))


def train_delivery(df):
    df = df.copy()
    encoder = LabelEncoder()
    df["shipping_method"] = encoder.fit_transform(df["shipping_method"])
    X, y = df[C.DELIVERY_FEATURES], df["delivery_risk"]
    X_train, X_test, y_train, y_test = _split(X, y)
    model = _new_model().fit(X_train, y_train)
    from .evaluation import evaluate
    return model, encoder, evaluate(y_test, model.predict(X_test))


def main(regenerate: bool = False) -> None:
    C.DATA_DIR.mkdir(exist_ok=True)
    C.MODEL_DIR.mkdir(exist_ok=True)

    if regenerate or not C.INVENTORY_CSV.exists() or not C.DELIVERY_CSV.exists():
        print("Generating synthetic datasets with a single continuous random stream...")
        inv_df, del_df = generate_both()
        inv_df.to_csv(C.INVENTORY_CSV, index=False)
        del_df.to_csv(C.DELIVERY_CSV, index=False)
        print(f"  Inventory: {len(inv_df)} rows, risk distribution: "
              f"{dict(inv_df['inventory_risk'].value_counts().sort_index())}")
        print(f"  Delivery:  {len(del_df)} rows, risk distribution: "
              f"{dict(del_df['delivery_risk'].value_counts().sort_index())}")
    else:
        import pandas as pd
        inv_df = pd.read_csv(C.INVENTORY_CSV)
        del_df = pd.read_csv(C.DELIVERY_CSV)

    print("\nTraining models...")
    inv_model, inv_metrics = train_inventory(inv_df)
    del_model, encoder, del_metrics = train_delivery(del_df)

    joblib.dump(inv_model, C.INVENTORY_MODEL)
    joblib.dump(del_model, C.DELIVERY_MODEL)
    joblib.dump(encoder, C.SHIPPING_ENCODER)
    C.METRICS_JSON.write_text(
        json.dumps({"inventory": inv_metrics, "delivery": del_metrics}, indent=2)
    )

    for name, m in (("Inventory", inv_metrics), ("Delivery", del_metrics)):
        print(f"\n=== {name} (synthetic held-out test, n={m['n_test']}) ===")
        print(f"accuracy={m['accuracy']:.4f}  precision={m['precision']:.4f}  "
              f"recall={m['recall']:.4f}  f1={m['f1']:.4f}")
        print(m["classification_report_text"])
    print("Saved:", C.INVENTORY_MODEL.name, C.DELIVERY_MODEL.name,
          C.SHIPPING_ENCODER.name, C.METRICS_JSON.name)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--regenerate", action="store_true",
                    help="regenerate synthetic CSVs (overwrites data/*.csv)")
    main(ap.parse_args().regenerate)
