import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Dashboard Configuration & Visual Hierarchy setup
st.set_page_config(layout="wide", page_title="Executive Business Dashboard")
st.title("📊 Interactive Dashboard & KPI Visualizations")
st.markdown("### Executive Performance Analysis Track")

# 1. Generate Mock Analytical Dataset
@st.cache_data
def get_mock_data():
    np.random.seed(42)
    dates = pd.date_range(start="2026-01-01", periods=90)
    sources = ["Google Ads", "Meta Ads", "Organic", "Email Link", "Referral"]
    countries = ["USA", "India", "UK", "Canada", "Germany", "Australia"]
    
    data = {
        "Date": np.random.choice(dates, size=500),
        "Customer_ID": [f"C{1000+i}" for i in range(500)],
        "Country": np.random.choice(countries, size=500),
        "Revenue": np.random.uniform(50, 500, size=500).round(2),
        "Marketing_Spend": np.random.uniform(10, 100, size=500).round(2),
        "Acquisition_Source": np.random.choice(sources, size=500),
        "Churn_Flag": np.random.choice([0, 1], size=500, p=[0.85, 0.15]),
        "Order_ID": [f"O{9000+i}" for i in range(500)]
    }
    return pd.DataFrame(data).sort_values("Date")

df = get_mock_data()

# 2. Interactive Filtering Slicers in Sidebar
st.sidebar.header("Temporal & Categorical Filters")
selected_sources = st.sidebar.multiselect("Acquisition Channels", options=df["Acquisition_Source"].unique(), default=df["Acquisition_Source"].unique())

# Drill-down Filtering Execution
filtered_df = df[df["Acquisition_Source"].isin(selected_sources)]

# 3. Mathematical Operations for Core KPIs
revenue_sum = filtered_df["Revenue"].sum()
unique_customers = filtered_df["Customer_ID"].nunique()
marketing_sum = filtered_df["Marketing_Spend"].sum()
orders_count = filtered_df["Order_ID"].nunique()
churned_count = filtered_df["Churn_Flag"].sum()

cac_metric = marketing_sum / unique_customers if unique_customers > 0 else 0
churn_rate_metric = (churned_count / unique_customers) * 100 if unique_customers > 0 else 0
aov_metric = revenue_sum / orders_count if orders_count > 0 else 0

# 4. Top Row Display: Summary Dashboard Metric Cards
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
kpi_col1.metric("Total Revenue", f"${revenue_sum:,.2f}")
kpi_col2.metric("Customer Acquisition Cost (CAC)", f"${cac_metric:,.2f}")
kpi_col3.metric("Churn Rate", f"{churn_rate_metric:.2f}%")
kpi_col4.metric("Average Order Value (AOV)", f"${aov_metric:,.2f}")

st.markdown("---")

# 5. Dual Visualization Columns
chart_left, chart_right = st.columns(2)

with chart_left:
    st.subheader("📈 Revenue Growth & Performance Trend")
    trend_data = filtered_df.groupby("Date")["Revenue"].sum().reset_index()
    trend_chart = px.area(trend_data, x="Date", y="Revenue", labels={"Revenue": "Daily Revenue ($)"})
    st.plotly_chart(trend_chart, use_container_width=True)

with chart_right:
    st.subheader("🗺️ Geographic Revenue Heatmap")
    geo_data = filtered_df.groupby("Country")["Revenue"].sum().reset_index()
    geo_heatmap = px.choropleth(geo_data, locations="Country", locationmode="country names", color="Revenue",
                                color_continuous_scale="Viridis", labels={"Revenue": "Total Revenue ($)"})
    st.plotly_chart(geo_heatmap, use_container_width=True)
