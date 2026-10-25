# SmartSupply AI — UI/UX Design Specification
## Synthetic Phase 1 • Streamlit • Random Forest Risk Intelligence

> **Product:** SmartSupply AI  
> **Tagline:** ML-Based Supply Chain Risk Intelligence  
> **Core principle:** **DATA → MODEL → RISK → ACTION**

---

## 1. Design Goal

SmartSupply AI should feel like a compact **supply-chain operations command center**, not a generic Streamlit project.

The interface must make four things immediately understandable:

1. What is happening?
2. What is risky?
3. What did the model predict?
4. What should the user inspect next?

This version uses **synthetic data**, so the interface must also communicate that clearly without making the product look like a toy.

### Product positioning

**Good:**  
> "Supply-chain risk intelligence powered by machine learning."

**Avoid:**  
> "Accurate real-world supply-chain prediction."

The supplied ML code creates synthetic targets using deterministic rules. The UI must never imply real-world validation.

---

# 2. Visual Direction

### Style

**Dark Operations Dashboard + Modern ML Analytics**

Blend:

- Enterprise logistics software
- SaaS analytics
- ML monitoring dashboards
- Operations control rooms

Avoid:

- Cyberpunk neon overload
- Huge gradients
- Decorative illustrations
- Excessive animation
- Giant marketing-style headings
- Generic Streamlit default styling

The design should look credible enough to evolve into a real product while remaining appropriate for a college ML mini-project.

---

# 3. Color System

| Purpose | Color |
|---|---|
| App background | `#0B1120` |
| Main surface | `#111827` |
| Elevated surface | `#172033` |
| Borders | `#243047` |
| Primary accent | `#38BDF8` |
| Primary text | `#F8FAFC` |
| Secondary text | `#CBD5E1` |
| Muted text | `#94A3B8` |
| Low risk | `#22C55E` |
| High risk | `#EF4444` |
| Warning/attention | `#F59E0B` |

### Rules

- Cyan/blue = navigation, selected state, primary actions.
- Green = LOW / NORMAL.
- Red = HIGH.
- Amber may be used for warnings or attention, but **not as a third ML class**.
- Always show risk text labels in addition to color.
- Do not color entire tables aggressively.
- Keep charts restrained.

---

# 4. Typography

Preferred:

1. Inter
2. Plus Jakarta Sans
3. System sans-serif fallback

| Element | Size |
|---|---:|
| Page title | 28–32px |
| Section title | 18–22px |
| KPI number | 24–30px |
| Body | 14–16px |
| Table | 13–14px |
| Caption | 12–13px |

Use semibold typography for headings and important values.

---

# 5. Application Shell

## Sidebar

Compact dark sidebar.

### Brand

**📦 SmartSupply AI**

Subtitle:

`Supply Chain Intelligence`

### Navigation

- Overview
- Inventory Risk
- Delivery Risk
- Model Performance

Do **not** show a Risk Map in this synthetic-data version.

If a future version adds reliable latitude/longitude fields, the navigation item can be enabled.

### Sidebar footer

```text
PHASE 1
SYNTHETIC ML PROTOTYPE
```

The active item should use:

- Cyan accent
- Slightly elevated background
- Rounded container
- Icon + text

---

# 6. Global Synthetic Data Banner

Every major dashboard view should make the dataset status clear.

Recommended banner:

> **SYNTHETIC DATASET**  
> Predictions and metrics shown here are generated from simulated data and rule-based labels for academic demonstration.

Keep this visually noticeable but not intrusive.

Do not use wording such as:

> "Production-ready predictions."

---

# 7. Overview Dashboard

## Header

### Title

**Supply Chain Command Center**

### Subtitle

`ML-powered inventory and delivery risk intelligence`

Optional status:

`● Models Ready`

Secondary status:

`Synthetic Dataset`

---

## KPI Row

Use four compact cards.

### Card 1

**Inventory Records**

Example:

`1,000`

Supporting text:

`Synthetic inventory records`

### Card 2

**Inventory High Risk**

Example:

`XXX`

Supporting text:

`Records classified HIGH`

### Card 3

**Delivery Records**

Example:

`1,000`

Supporting text:

`Synthetic delivery records`

### Card 4

**Delivery High Risk**

Example:

`XXX`

Supporting text:

`Records classified HIGH`

> Never hard-code the example values. Calculate them from the generated/test data.

---

# 8. Risk Summary

Use two equal-width panels.

## Inventory Risk Distribution

Recommended:

- Donut chart or bar chart
- LOW
- HIGH

Because the supplied target is binary, do not invent a MEDIUM class.

Under the chart:

`XXX high-risk inventory records`

## Delivery Risk Distribution

Same visual language.

Under the chart:

`XXX high-risk delivery records`

---

# 9. Priority Attention

Section title:

**Priority Attention**

Show the most important synthetic records based on model prediction probability when available.

### Inventory table

| Record | Stock | Demand | Lead Time | Previous Stockouts | Risk |
|---|---:|---:|---:|---:|---|
| INV-XXXX | 42 | 20 | 12 | 3 | HIGH |

### Delivery table

| Record | Distance | Processing | Shipping | Delay Rate | Risk |
|---|---:|---:|---|---:|---|
| ORD-XXXX | 760 km | 12 | Standard | 0.71 | HIGH |

If record IDs are not present in the supplied dataset, generate **display-only row identifiers** such as `INV-0001` and `ORD-0001`. Clearly treat them as UI identifiers, not source-system IDs.

---

# 10. Inventory Risk Page

## Header

**Inventory Risk Intelligence**

Subtitle:

`Identify synthetic inventory records classified as stockout risk.`

---

## KPI Row

Display:

- Total Inventory Records
- High Risk
- Average Stock
- Average Daily Demand

---

## Filters

Use a compact filter bar.

Supported filters:

- Risk
- Current stock range
- Daily demand range
- Supplier lead time range
- Previous stockout range

Do not add category, supplier, warehouse, or product filters because those fields do not exist in the supplied dataset.

---

# 11. Inventory Charts

## Chart A — Risk Distribution

Bar or donut:

- LOW
- HIGH

## Chart B — Stock vs Demand

Scatter plot:

- X = Daily Demand
- Y = Current Stock
- Symbol/category = predicted risk

Optional reference line:

`Current Stock = Daily Demand × 3`

This line is particularly useful because the synthetic target-generation rule marks inventory as risky when current stock falls below three days of demand.

Label the line clearly:

> Synthetic label rule reference

Do not describe it as a learned threshold.

---

# 12. Inventory Prediction Card

## Title

**Predict Inventory Risk**

Inputs:

- Current Stock
- Daily Demand
- Supplier Lead Time
- Previous Stockouts
- Sales Last 7 Days

Primary button:

**Analyze Inventory Risk**

---

## Result State

Example:

```text
HIGH RISK

Model prediction: 1
Model probability: 82%

The Random Forest classifies this record as high inventory risk.
```

Probability should come from:

`model.predict_proba(...)`

Do not call it:

- "82% chance of real-world stockout"
- "82% certainty"
- "82% guaranteed accuracy"

Use:

> **Model probability**

---

# 13. Inventory Risk Indicators

Because the synthetic target is generated from explicit rules, the UI may show a small panel:

### Synthetic Label Conditions

- Low stock coverage
- Long supplier lead time
- Repeated previous stockouts

Example:

```text
Triggered conditions
✓ Stock below 3× daily demand
✓ Supplier lead time above 10 days
○ Previous stockouts below threshold
```

Important:

> These are the synthetic dataset's label-generation rules, not explanations produced by the Random Forest.

This distinction should be visible in the UI or tooltip.

---

# 14. Delivery Risk Page

## Header

**Delivery Risk Intelligence**

Subtitle:

`Identify synthetic orders classified as delivery-delay risk.`

---

## KPI Row

Display:

- Total Delivery Records
- High Risk
- Average Distance
- Average Processing Time

---

# 15. Delivery Filters

Supported:

- Risk
- Shipping Method
- Distance
- Processing Time
- Warehouse Delay Rate

Do not add:

- Region
- Warehouse
- Destination
- Driver
- Vehicle

because those fields do not exist in the supplied dataset.

---

# 16. Delivery Charts

## Chart A — Risk Distribution

Show:

- LOW
- HIGH

## Chart B — Distance vs Processing Time

Scatter plot:

- X = Distance km
- Y = Processing Time
- Risk = predicted class

Optional reference lines:

- Distance = 500 km
- Processing Time = 10

Label them:

> Synthetic label rule reference

These are not learned decision boundaries.

---

# 17. Delivery Prediction Card

## Title

**Predict Delivery Risk**

Inputs:

- Distance (km)
- Processing Time
- Order Value
- Warehouse Delay Rate
- Shipping Method

Shipping method options:

- Standard
- Express

Primary button:

**Analyze Delivery Risk**

---

## Result

```text
HIGH RISK

Model prediction: 1
Model probability: 76%

The Random Forest classifies this delivery record as high risk.
```

The application must encode `shipping_method` using the saved:

`shipping_encoder.pkl`

before calling the model.

---

# 18. Delivery Risk Indicators

Optional panel:

### Synthetic Label Conditions

- Distance above 500 km
- Processing time above 10
- Warehouse delay rate above 0.6

Example:

```text
Triggered conditions
✓ Distance above 500 km
○ Processing time within threshold
✓ Warehouse delay rate above 0.6
```

Again:

> These are dataset-generation rules, not model explanations.

---

# 19. Model Performance Page

This page is the main academic evidence screen.

## Header

**Model Performance**

Subtitle:

`Random Forest evaluation on synthetic held-out test data`

---

## Model Cards

### Inventory Model

```text
Random Forest
100 estimators
80/20 train-test split
Random state: 42
```

### Delivery Model

```text
Random Forest
100 estimators
80/20 train-test split
Random state: 42
```

---

# 20. Metrics

Display the actual output of:

- Accuracy
- Precision
- Recall
- F1-score

The supplied code uses:

- `accuracy_score`
- `classification_report`

Do not invent values.

### Important UI note

Use a small disclaimer:

> High performance is expected because the target labels are generated from explicit synthetic rules. These metrics do not represent real-world model performance.

---

# 21. Confusion Matrix

Provide selectors:

```text
Dataset
[ Inventory ▼ ]

Model
[ Random Forest ▼ ]
```

Show:

- Actual
- Predicted
- Class 0 / Low
- Class 1 / High

Recommended visualization:

- Plotly heatmap
- Dark background
- Clear numeric annotations

---

# 22. Feature Importance

Because the model is Random Forest, display:

**Random Forest Feature Importance**

### Inventory

Potential features:

- current_stock
- daily_demand
- supplier_lead_time
- previous_stockouts
- sales_last_7_days

### Delivery

Potential features:

- distance_km
- processing_time
- order_value
- warehouse_delay_rate
- shipping_method

The chart must be generated from:

`model.feature_importances_`

Never manually assign importance values.

Recommended chart:

**Horizontal bar chart**

Sort descending.

---

# 23. Model Architecture Visual

A compact architecture card can appear on the Model Performance page.

```text
SYNTHETIC DATA
      ↓
RULE-BASED TARGET
      ↓
TRAIN / TEST SPLIT
      ↓
RANDOM FOREST
      ↓
CLASSIFICATION
      ↓
METRICS + RISK
```

This helps evaluators understand the project immediately.

---

# 24. Risk System

The supplied ML target is binary.

## LOW

```text
Prediction = 0
```

Meaning:

`Normal synthetic operating risk`

## HIGH

```text
Prediction = 1
```

Meaning:

`Elevated synthetic operating risk`

### Important

Do not make the model appear to predict:

- LOW
- MEDIUM
- HIGH

unless a future version explicitly adds a three-class target.

Amber can still be used for interface warnings or attention states without becoming a third ML class.

---

# 25. Prediction UX

Use this flow:

```text
INPUT
  ↓
VALIDATE
  ↓
ENCODE / FORMAT
  ↓
RANDOM FOREST
  ↓
PREDICTION
  ↓
MODEL PROBABILITY
  ↓
RISK CARD
```

When the user clicks the button:

1. Validate numeric ranges.
2. Validate required fields.
3. Encode shipping method if delivery prediction is selected.
4. Load the saved model.
5. Generate class prediction.
6. Generate probability if available.
7. Show LOW/HIGH result.
8. Optionally show synthetic rule indicators.

---

# 26. Input Validation

Inventory:

- Current stock ≥ 0
- Daily demand ≥ 0
- Supplier lead time ≥ 0
- Previous stockouts ≥ 0
- Sales last 7 days ≥ 0

Delivery:

- Distance ≥ 0
- Processing time ≥ 0
- Order value ≥ 0
- Warehouse delay rate between 0 and 1
- Shipping method must be Standard or Express

Show validation next to the relevant input.

Never expose raw Python exceptions.

---

# 27. Empty and Error States

## Model unavailable

Show:

> **Model Not Available**  
> Train the model before using prediction features.

## Invalid input

Show:

> **Invalid Input**  
> Please check the highlighted fields.

## Empty filtered table

Show:

> **No Matching Records**  
> No records match the selected filters.

## Missing data

Show:

> **Synthetic Dataset Unavailable**  
> Generate or load the dataset before opening this view.

---

# 28. No Risk Map in Synthetic Phase 1

The current data has no:

- latitude
- longitude
- warehouse
- destination
- region

Therefore:

**Do not build a map.**

Do not create random coordinates just to satisfy a dashboard requirement.

Instead, use the available operational visualizations:

- Risk distribution
- Stock vs demand
- Distance vs processing time
- Feature importance
- High-risk tables

A real map becomes valid only when reliable geographic data is introduced.

---

# 29. Component System

Create reusable UI components conceptually equivalent to:

```text
KpiCard
RiskBadge
SyntheticDataBanner
PredictionCard
SectionHeader
RiskDistribution
HighRiskTable
FeatureImportance
ConfusionMatrix
MetricCard
FilterBar
```

All components should share:

- Border radius
- Padding
- Typography
- Spacing
- Risk-state treatment

---

# 30. Cards

Recommended:

- Radius: 12–16px
- Background: `#111827` or `#172033`
- Border: `#243047`
- Padding: 16–20px
- Minimal shadow

Avoid excessive glassmorphism.

The interface should feel operational and dense enough for analytics.

---

# 31. Buttons

Primary:

- Cyan/blue accent
- Dark readable text
- 8–10px radius

Examples:

**Analyze Inventory Risk**

**Analyze Delivery Risk**

**Refresh Analysis**

Avoid oversized CTA buttons.

---

# 32. Tables

Tables should be:

- Compact
- Sortable where practical
- Filterable
- Horizontally scrollable if necessary

Use risk badges:

`LOW`

`HIGH`

Do not color the entire row red.

---

# 33. Charts

Use Plotly where practical.

Recommended:

1. Inventory risk distribution
2. Delivery risk distribution
3. Stock vs demand
4. Distance vs processing time
5. Confusion matrix
6. Random Forest feature importance

Rules:

- Dark background
- Subtle gridlines
- Cyan/blue for analytical series
- Red/green reserved for risk states
- No 3D charts
- No unnecessary animation

---

# 34. Responsive Layout

Prioritize:

1. Page title
2. Synthetic-data banner
3. KPIs
4. Risk summary
5. Prediction card
6. Tables
7. Secondary charts

The app should remain usable on:

- Laptop
- Desktop
- Smaller desktop window

Do not make text unreadably small.

---

# 35. Streamlit Architecture

Recommended separation:

```text
app.py
    ↓
UI / page routing
    ↓
prediction.py
    ↓
saved .pkl artifacts

training code
    ↓
synthetic data
    ↓
Random Forest
    ↓
saved models
```

The Streamlit application should **not retrain the models every time a user changes a widget**.

Prefer:

```text
Train once
   ↓
Save artifacts
   ↓
Streamlit loads artifacts
   ↓
Inference
```

---

# 36. Artifact Contract

The dashboard expects:

```text
models/
├── inventory_model.pkl
├── delivery_model.pkl
└── shipping_encoder.pkl
```

### Inventory model input order

```text
current_stock
daily_demand
supplier_lead_time
previous_stockouts
sales_last_7_days
```

### Delivery model input order

```text
distance_km
processing_time
order_value
warehouse_delay_rate
shipping_method
```

The Streamlit prediction code must preserve the same feature order used during training.

---

# 37. Accessibility

Use:

- High text contrast
- Labels + icons
- Risk text in addition to colors
- Readable chart labels
- Clear form labels
- Meaningful buttons

Do not rely on red/green alone.

---

# 38. Phase 1 Boundaries

Do not build yet:

- Real-time GPS
- Live traffic
- Live weather
- Route optimization
- Automatic purchasing
- Supplier negotiation
- Chatbot
- AI agent
- Authentication
- Multi-tenant architecture
- Real-time database
- Production monitoring
- Fake map coordinates
- Real-world accuracy claims

---

# 39. Future Product Direction

```text
PHASE 1
Synthetic Risk Classification
        ↓
PHASE 2
Real Dataset + Model Comparison
        ↓
PHASE 3
Demand Forecasting + Supplier Risk
        ↓
PHASE 4
Geographic / Route Risk
        ↓
PHASE 5
Optimization + Explainable AI
        ↓
PHASE 6
Supply Chain AI Copilot
```

Potential future modules:

- Demand forecasting
- Supplier reliability
- Route risk
- Safety-stock recommendations
- ETA prediction
- SHAP explanations
- What-if simulation
- Automated alerts
- Model monitoring
- FastAPI backend
- Database
- Docker
- Cloud deployment

---

# 40. Final Product Principle

SmartSupply AI should not feel like:

> "A Random Forest model wrapped in Streamlit."

It should feel like:

> **"A compact supply-chain operations intelligence product powered by machine learning."**

The UI hierarchy:

**KPI → RISK → RECORDS → PREDICTION → MODEL EVIDENCE**

The technical hierarchy:

**SYNTHETIC DATA → RULE-BASED LABEL → RANDOM FOREST → PREDICTION → EVALUATION**
