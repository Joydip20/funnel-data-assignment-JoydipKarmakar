# funnel-data-assignment-JoydipKarmakar

Short assignment: SQL + Python for session & order analytics.

## ✅ Requirements
- Python 3.9+
- pip install -r requirements.txt

```
pip install -r requirements.txt
```

## 🏃 Quickstart

1) Place the CSVs (events.csv, messages.csv, orders.csv, products.csv, inventory.csv) anywhere on disk.

2) Run the report script (outputs to ./out by default):

```
python src/evo_report.py --events /path/events.csv --messages /path/messages.csv --orders /path/orders.csv --out ./out/
```

3) Inspect outputs in `/out`:
- `report.json`
- `funnel.png` (grouped by device)
- `intents.png` (top 10)

## 📦 SQL
Three reference queries are in `/sql`:
- `funnel.sql`
- `intent_distribution.sql`
- `cancellation_sla.sql`

They are ANSI/SQLite-friendly; adjust for your warehouse as needed.

## 📝 Assumptions
- Funnel is by **distinct users** per device; steps are `Loaded → Interact → Clicks → Purchase`.
- Intent `NULL/''` → `unknown`.
- Cancellation SLA violation: `canceled_at - created_at > 60 minutes`.
- Timestamps are UTC and parsable as `YYYY-MM-DD HH:MM:SS`.

## 🗂 Structure
```
/sql
  funnel.sql
  intent_distribution.sql
  cancellation_sla.sql
/src
  evo_report.py
/out
  (generated files)
INSIGHTS.md
README.md
```

