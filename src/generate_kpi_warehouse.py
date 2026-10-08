import pandas as pd, numpy as np, os
from datetime import timedelta
os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/warehouse", exist_ok=True)
np.random.seed(10)

# DIMENSIONS
dim_date = pd.DataFrame({"date": pd.date_range("2023-01-01","2025-10-08")})
dim_date["date_key"] = dim_date["date"].dt.strftime("%Y%m%d").astype(int)
dim_date["month"] = dim_date["date"].dt.to_period("M").astype(str)
dim_date["quarter"] = dim_date["date"].dt.quarter
dim_date["year"] = dim_date["date"].dt.year

dim_customer = pd.DataFrame({
  "customer_key": range(1,5001),
  "customer_id": [f"U_{i}" for i in range(5000)],
  "segment": np.random.choice(["Premium","Growth","SMB","Churn Risk"],5000,p=[0.2,0.3,0.3,0.2]),
  "region": np.random.choice(["Lagos","PH","Abuja","Kano","IB"],5000)
})

dim_product = pd.DataFrame({
  "product_key": [1,2,3],
  "product": ["Transfer","Savings","Loan"],
  "revenue_model": ["fee","interest","interest"]
})

# FACT TABLE — daily KPIs
facts=[]
for d in dim_date["date"].sample(600): # 600 days
  for seg in ["Premium","Growth","SMB","Churn Risk"]:
    revenue = int(np.random.normal(800000 if seg=="Premium" else 300000, 80000))
    active_users = int(np.random.normal(1200 if seg=="Premium" else 600, 100))
    churned = int(np.random.normal(15 if seg=="Churn Risk" else 5, 3))
    activated = int(np.random.normal(80 if seg=="Growth" else 40, 15))
    facts.append({
      "date_key": int(d.strftime("%Y%m%d")),
      "segment": seg,
      "revenue_ngn": max(0,revenue),
      "active_users": max(0,active_users),
      "churned_users": max(0,churned),
      "activated_users": max(0,activated),
      "arpu": revenue/max(1,active_users)
    })

fact_kpi = pd.DataFrame(facts)
fact_kpi.to_csv("data/warehouse/fact_daily_kpi.csv", index=False)
dim_date.to_csv("data/warehouse/dim_date.csv", index=False)
dim_customer.to_csv("data/warehouse/dim_customer.csv", index=False)
dim_product.to_csv("data/warehouse/dim_product.csv", index=False)
print(f"Star schema built: fact {len(fact_kpi)} rows, {len(dim_customer)} customers")
