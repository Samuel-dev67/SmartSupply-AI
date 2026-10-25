"""Synthetic data generation for SmartSupply AI (Phase 1).

Uses a SINGLE continuous random stream (np.random.seed(42) called once before
the entire generation sequence) to exactly reproduce the original prototype's data.

Generation order must be preserved:
  1. np.random.seed(42)
  2. Inventory features + labels
  3. Delivery features + labels

Never call np.random.seed() again inside these functions or between them.

TARGET RULES are the source-of-truth label logic and must not change.
"""
import numpy as np
import pandas as pd

from .config import N_RECORDS, SEED, SHIPPING_METHODS


# ---------------------------------------------------------------------------
# Label-rule functions (source of truth — do NOT change)
# ---------------------------------------------------------------------------

def inventory_target(df: pd.DataFrame) -> pd.Series:
    """Synthetic label rule for inventory risk (1 = HIGH)."""
    return (
        (df["current_stock"] < df["daily_demand"] * 3)
        | (df["supplier_lead_time"] > 10)
        | (df["previous_stockouts"] >= 3)
    ).astype(int)


def delivery_target(df: pd.DataFrame) -> pd.Series:
    """Synthetic label rule for delivery risk (1 = HIGH)."""
    return (
        (df["distance_km"] > 500)
        | (df["processing_time"] > 10)
        | (df["warehouse_delay_rate"] > 0.6)
    ).astype(int)


# ---------------------------------------------------------------------------
# Joint generator — single continuous random stream
# ---------------------------------------------------------------------------

def generate_both(n: int = N_RECORDS, seed: int = SEED):
    """Generate inventory and delivery DataFrames from one shared random stream.

    The seed is set exactly once before any generation call, matching the
    original prototype's np.random.seed(42) followed by sequential randint calls.

    Returns:
        (inventory_df, delivery_df)
    """
    np.random.seed(seed)  # Single seed — called ONCE

    # --- Inventory features (authoritative ranges) ---
    current_stock       = np.random.randint(5,   200, n)
    daily_demand        = np.random.randint(1,    30, n)
    supplier_lead_time  = np.random.randint(1,    15, n)
    previous_stockouts  = np.random.randint(0,     6, n)
    sales_last_7_days   = np.random.randint(10,  250, n)

    inventory = pd.DataFrame({
        "current_stock":      current_stock,
        "daily_demand":       daily_demand,
        "supplier_lead_time": supplier_lead_time,
        "previous_stockouts": previous_stockouts,
        "sales_last_7_days":  sales_last_7_days,
    })
    inventory["inventory_risk"] = inventory_target(inventory)

    # --- Delivery features (authoritative ranges, stream continues) ---
    distance_km           = np.random.randint(5,     1000, n)
    processing_time       = np.random.randint(1,       15, n)
    order_value           = np.random.randint(500,  50000, n)
    warehouse_delay_rate  = np.random.uniform(0,        1, n)
    shipping_method       = np.random.choice(SHIPPING_METHODS, n)

    delivery = pd.DataFrame({
        "distance_km":          distance_km,
        "processing_time":      processing_time,
        "order_value":          order_value,
        "warehouse_delay_rate": warehouse_delay_rate,
        "shipping_method":      shipping_method,
    })
    delivery["delivery_risk"] = delivery_target(delivery)

    return inventory, delivery


# ---------------------------------------------------------------------------
# Convenience wrappers (used by train_models.py)
# ---------------------------------------------------------------------------

def generate_inventory(n: int = N_RECORDS, seed: int = SEED) -> pd.DataFrame:
    """Generate only the inventory DataFrame (re-seeds; use generate_both for
    the canonical joint stream)."""
    inv, _ = generate_both(n=n, seed=seed)
    return inv


def generate_delivery(n: int = N_RECORDS, seed: int = SEED) -> pd.DataFrame:
    """Generate only the delivery DataFrame (re-seeds; use generate_both for
    the canonical joint stream)."""
    _, dlv = generate_both(n=n, seed=seed)
    return dlv
