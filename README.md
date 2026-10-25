# SmartSupply AI — Phase 1 (Synthetic ML Prototype)

Supply-chain risk dashboard with two independent Random Forest classifiers
(Inventory Risk, Delivery Risk).

**All data and labels are synthetic and rule-generated.**  
Metrics do not represent real-world performance; this is an academic prototype,
not a production system.  
Targets are binary: `0 = LOW/NORMAL`, `1 = HIGH`.

## Quick Start

```bash
pip install -r requirements.txt
python -m src.train_models          # train once → writes models/*.pkl and models/metrics.json
streamlit run app.py                # loads saved artifacts; never retrains
```

Add `--regenerate` to overwrite `data/*.csv` with freshly generated data:

```bash
python -m src.train_models --regenerate
```

## Synthetic Data

The dataset is generated from a **single continuous random stream**
(`np.random.seed(42)` is called once before all feature generation calls,
in the order: inventory features → inventory labels → delivery features →
delivery labels). The ranges exactly match the original prototype:

### Inventory

| Feature | Generator |
|---|---|
| `current_stock` | `randint(5, 200)` |
| `daily_demand` | `randint(1, 30)` |
| `supplier_lead_time` | `randint(1, 15)` |
| `previous_stockouts` | `randint(0, 6)` |
| `sales_last_7_days` | `randint(10, 250)` |

Label rule (1 = HIGH risk):

```python
(current_stock < daily_demand * 3) | (supplier_lead_time > 10) | (previous_stockouts >= 3)
```

### Delivery

| Feature | Generator |
|---|---|
| `distance_km` | `randint(5, 1000)` |
| `processing_time` | `randint(1, 15)` |
| `order_value` | `randint(500, 50000)` |
| `warehouse_delay_rate` | `uniform(0, 1)` |
| `shipping_method` | `choice(["Standard", "Express"])` |

Label rule (1 = HIGH risk):

```python
(distance_km > 500) | (processing_time > 10) | (warehouse_delay_rate > 0.6)
```

## Models

Both classifiers use:

```python
RandomForestClassifier(n_estimators=100, random_state=42)
train_test_split(test_size=0.2, random_state=42)
```

`shipping_method` is encoded with a fitted `LabelEncoder` saved as
`models/shipping_encoder.pkl`.

## Layout

| Path | Purpose |
|---|---|
| `src/config.py` | Paths, feature order, constants |
| `src/data_generator.py` | Synthetic data + label rules |
| `src/train_models.py` | Training, evaluation, artifact saving (CLI only) |
| `src/evaluation.py` | Metrics / feature importance helpers |
| `src/predict.py` | Artifact loading, validation, inference |
| `ui/` | Theme, components, charts, pages |
| `app.py` | Shell and routing |

## Artifacts

```
models/
├── inventory_model.pkl    # fitted RandomForestClassifier
├── delivery_model.pkl     # fitted RandomForestClassifier
├── shipping_encoder.pkl   # fitted LabelEncoder
└── metrics.json           # accuracy, precision, recall, F1, confusion matrix
```

## Important Notes

- `src/train_models.py` is a CLI script and is **never imported by the Streamlit UI**.
  Widget reruns do not retrain the models.
- The Streamlit app uses `@st.cache_resource` / `@st.cache_data` to load artifacts once.
- No map is included because the dataset has no geographic fields (no latitude,
  longitude, warehouse, destination, or region).
- High performance metrics are expected: because the target labels are generated
  from deterministic rules, the Random Forest can learn those rules almost perfectly.
  These metrics do **not** indicate real-world predictive accuracy.
