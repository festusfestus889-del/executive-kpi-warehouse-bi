# Executive KPI Warehouse + Semantic Layer + BI

**Problem:** CEO gets 3 different churn numbers from 3 teams. KPI war.

**Solution:**
1. Star Schema: dim_date, dim_customer, dim_product, fact_daily_kpi (600 days)
2. Semantic Layer: `metrics/semantic_layer.yaml` — revenue, churn_rate, activation_rate, arpu defined once, owned by finance
3. BI: Streamlit exec dashboard — Revenue, Churn (alert >7%), Activation, ARPU by segment/month
4. Governance: churn_rate = churned/active <5% target, single source

**Stack:** Python, Pandas, YAML semantic layer, Plotly, Streamlit, GitHub Actions 7am

**Run:** streamlit run app.py
