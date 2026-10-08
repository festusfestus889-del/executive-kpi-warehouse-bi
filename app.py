import streamlit as st, pandas as pd, plotly.express as px
st.set_page_config(layout="wide", page_title="Executive KPI Warehouse")
st.title("💼 Executive KPI Warehouse + Semantic Layer")

monthly = pd.read_csv("data/processed/monthly_kpi.csv")
segment = pd.read_csv("data/processed/segment_kpi.csv")

# TOP KPIs
c1,c2,c3,c4 = st.columns(4)
c1.metric("Revenue (MTD)", f"₦{monthly['revenue'].iloc[-1]/1e6:.1f}M", f"{(monthly['revenue'].iloc[-1]/monthly['revenue'].iloc[-2]-1)*100:.1f}%")
c2.metric("Churn Rate", f"{monthly['churn_rate'].iloc[-1]*100:.1f}%", f"{(monthly['churn_rate'].iloc[-1]-monthly['churn_rate'].iloc[-2])*100:.1f}pp", delta_color="inverse")
c3.metric("Activation Rate", f"{monthly['activation_rate'].iloc[-1]*100:.0f}%")
c4.metric("ARPU", f"₦{monthly['arpu'].iloc[-1]:,.0f}")

st.plotly_chart(px.line(monthly, x="month", y="revenue", title="Revenue Trend — Star Schema: fact_daily_kpi"), use_container_width=True)

col1,col2 = st.columns(2)
col1.plotly_chart(px.bar(monthly, x="month", y="churn_rate", title="Churn Rate (Target <5%) — Alert if >7%", color="churn_rate", color_continuous_scale="Reds"), use_container_width=True)
col2.plotly_chart(px.bar(segment, x="segment", y="revenue", color="segment", title="Revenue by Segment — Dimension: dim_customer.segment"), use_container_width=True)

st.subheader("Semantic Layer — Single Source of Truth")
st.code("""
metrics:
  revenue: SUM(revenue_ngn) — owner: finance@company.com
  churn_rate: SUM(churned)/SUM(active) — target <5%
  activation_rate: SUM(activated)/SUM(active) — target 65%
""", language="yaml")

st.dataframe(monthly.tail(12), use_container_width=True)
st.success("Warehouse: dim_date, dim_customer, dim_product, fact_daily_kpi | Semantic layer prevents KPI wars")
