import pandas as pd, yaml, os
os.makedirs("data/processed", exist_ok=True)

fact = pd.read_csv("data/warehouse/fact_daily_kpi.csv")
dim_date = pd.read_csv("data/warehouse/dim_date.csv")

# Load semantic definitions
with open("metrics/semantic_layer.yaml") as f:
  sem = yaml.safe_load(f)

# Monthly exec summary
merged = pd.merge(fact, dim_date[["date_key","month","year","quarter"]], on="date_key")
monthly = merged.groupby("month").agg(
  revenue=("revenue_ngn","sum"),
  active=("active_users","sum"),
  churned=("churned_users","sum"),
  activated=("activated_users","sum")
).reset_index()
monthly["churn_rate"] = monthly["churned"]/monthly["active"]
monthly["activation_rate"] = monthly["activated"]/monthly["active"]
monthly["arpu"] = monthly["revenue"]/monthly["active"]
monthly.to_csv("data/processed/monthly_kpi.csv", index=False)

segment = merged.groupby("segment").agg(
  revenue=("revenue_ngn","sum"),
  active=("active_users","sum"),
  churn_rate=("churned_users","sum")
).reset_index()
segment["churn_rate"] = segment["churn_rate"]/segment["active"]
segment.to_csv("data/processed/segment_kpi.csv", index=False)

print(monthly.tail())
print("Semantic layer:", list(sem["metrics"].keys()))
