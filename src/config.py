"""Shared constants. Single source of truth for paths, feature order and label rules."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
MODEL_DIR = ROOT / "models"

INVENTORY_CSV = DATA_DIR / "inventory.csv"
DELIVERY_CSV = DATA_DIR / "delivery.csv"
INVENTORY_MODEL = MODEL_DIR / "inventory_model.pkl"
DELIVERY_MODEL = MODEL_DIR / "delivery_model.pkl"
SHIPPING_ENCODER = MODEL_DIR / "shipping_encoder.pkl"
METRICS_JSON = MODEL_DIR / "metrics.json"

# Feature order MUST match training and inference.
INVENTORY_FEATURES = [
    "current_stock",
    "daily_demand",
    "supplier_lead_time",
    "previous_stockouts",
    "sales_last_7_days",
]
DELIVERY_FEATURES = [
    "distance_km",
    "processing_time",
    "order_value",
    "warehouse_delay_rate",
    "shipping_method",
]

SHIPPING_METHODS = ["Standard", "Express"]

N_RECORDS = 1000
SEED = 42
TEST_SIZE = 0.2
N_ESTIMATORS = 100
