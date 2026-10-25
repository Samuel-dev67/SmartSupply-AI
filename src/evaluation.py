"""Evaluation helpers. Pure functions, no I/O and no Streamlit."""
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)


def evaluate(y_true, y_pred) -> dict:
    """Metrics for the binary task (positive class = 1 = HIGH)."""
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "classification_report": classification_report(
            y_true, y_pred, output_dict=True, zero_division=0
        ),
        "classification_report_text": classification_report(
            y_true, y_pred, zero_division=0
        ),
        "confusion_matrix": confusion_matrix(y_true, y_pred, labels=[0, 1]).tolist(),
        "n_test": int(len(y_true)),
    }


def feature_importance(model, feature_names) -> pd.DataFrame:
    """Importances straight from model.feature_importances_, sorted descending."""
    df = pd.DataFrame(
        {"feature": list(feature_names), "importance": np.asarray(model.feature_importances_)}
    )
    return df.sort_values("importance", ascending=False).reset_index(drop=True)
