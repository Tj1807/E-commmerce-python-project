import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

@st.cache_data
def load_data():
    df = pd.read_csv("ecommerce_returns_synthetic_data.csv")
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    df["Return_Date"] = pd.to_datetime(df["Return_Date"], errors="coerce")
    df["Days_to_Return"] = pd.to_numeric(df["Days_to_Return"], errors="coerce").abs()
    df["Revenue"] = df["Product_Price"] * df["Order_Quantity"]
    return df

# === EXISTING PLOT FUNCTIONS ===
def plot_return_rate(df):
    return_rate = df["Return_Status"].value_counts(normalize=True) * 100
    fig = px.bar(return_rate, x=return_rate.index, y=return_rate.values,
                 labels={"x": "Return Status", "y": "Percentage"},
                 title="Overall Return Rate (%)")
    return fig

def plot_category_return_percentage(df):
    cat_returns = (df.groupby("Product_Category")["Return_Status"]
                   .value_counts(normalize=True).unstack().fillna(0) * 100)
    fig = px.bar(cat_returns["Returned"], x=cat_returns.index, y=cat_returns["Returned"],
                 labels={"x": "Product Category", "y": "Return %"},
                 title="Return % by Product Category")
    return fig

# === NEW PLOT FUNCTIONS ===
def plot_return_reason_pie(df):
    reason_counts = df[df["Return_Status"] == "Returned"]["Return_Reason"].value_counts()
    fig = px.pie(values=reason_counts.values, names=reason_counts.index,
                 title="Return Reasons Distribution (%)", hole=0.4)
    return fig

def plot_revenue_histogram(df):
    fig = px.histogram(df, x="Revenue", nbins=30,
                       title="Revenue Distribution",
                       labels={"Revenue": "Revenue ($)"})
    fig.update_layout(bargap=0.1)
    return fig

def plot_price_vs_days_scatter(df):
    scatter_df = df[df["Return_Status"] == "Returned"].dropna(subset=["Days_to_Return"])
    fig = px.scatter(scatter_df, x="Product_Price", y="Days_to_Return",
                     color="Product_Category", size="Order_Quantity",
                     hover_data=["Return_Reason"],
                     title="Price vs Days to Return (Returns Only)",
                     labels={"Product_Price": "Product Price ($)", "Days_to_Return": "Days to Return"})
    return fig

def plot_category_revenue_pie(df):
    cat_revenue = df.groupby("Product_Category")["Revenue"].sum().round(0)
    fig = px.pie(values=cat_revenue.values, names=cat_revenue.index,
                 title="Total Revenue by Product Category")
    return fig

def main():
    st.set_page_config(page_title="E-commerce Returns Dashboard", layout="wide")
    st.title("🛒 E-commerce Returns Analytics")

    df = load_data()

    # === FIXED DYNAMIC FILTERS ===
    st.header("🔧 Dynamic Filters")
    
    # Row 1: Dropdowns
    col1, col2 = st.columns(2)
    with col1:
        selected_category = st.selectbox(
            "Product Category", 
            ["All"] + sorted(df["Product_Category"].unique().tolist())
        )
    with col2:
        selected_gender = st.selectbox(
            "User Gender", 
            ["All"] + sorted(df["User_Gender"].unique().tolist())
        )
    
    # Row 2: Sliders
    col3, col4 = st.columns(2)
    with col3:
        min_age, max_age = st.slider(
            "User Age Range", min_value=18, max_value=70, value=(25, 55), step=1
        )
    with col4:
        min_revenue, max_revenue = st.slider(
            "Revenue Range ($)", min_value=0, max_value=3000, value=(200, 1500), step=50
        )
    
    # Row 3: Slicers
    col5, col6 = st.columns(2)
    with col5:
        days_options = sorted(df["Days_to_Return"].dropna().unique())[:15]
        min_days, max_days = st.select_slider(
            "Days to Return", options=days_options,
            value=(days_options[3], days_options[10])
        )
    with col6:
        selected_reason = st.multiselect(
            "Return Reason", default=[],
            options=sorted(df["Return_Reason"].dropna().unique().tolist())
        )
    
    # === APPLY FILTERS ===
    filtered_df = df.copy()
    
    if selected_category != "All":
        filtered_df = filtered_df[filtered_df["Product_Category"] == selected_category]
    if selected_gender != "All":
        filtered_df = filtered_df[filtered_df["User_Gender"] == selected_gender]
    
    filtered_df = filtered_df[
        (filtered_df["User_Age"] >= min_age) & 
        (filtered_df["User_Age"] <= max_age)
    ]
    
    filtered_df = filtered_df[
        (filtered_df["Revenue"] >= min_revenue) & 
        (filtered_df["Revenue"] <= max_revenue)
    ]
    
    if len(filtered_df) > 0 and not filtered_df["Days_to_Return"].isna().all():
        filtered_df = filtered_df[
            (filtered_df["Days_to_Return"] >= min_days) & 
            (filtered_df["Days_to_Return"] <= max_days)
        ]
    
    if selected_reason:
        filtered_df = filtered_df[filtered_df["Return_Reason"].isin(selected_reason)]
    
    # === DASHBOARD ===
    st.header("📊 Interactive Analytics")
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    total_orders = len(filtered_df)
    returned_orders = len(filtered_df[filtered_df["Return_Status"] == "Returned"])
    return_rate = (returned_orders / total_orders * 100) if total_orders > 0 else 0
    
    with col1: st.metric("Total Orders", total_orders)
    with col2: st.metric("Returned Orders", returned_orders)
    with col3: st.metric("Return Rate", f"{return_rate:.1f}%")
    with col4:
        avg_days = filtered_df["Days_to_Return"].mean()
        st.metric("Avg Days to Return", f"{avg_days:.0f}" if not pd.isna(avg_days) else "N/A")
    
    # === TABS WITH 6 CHARTS (NEW) ===
    tab1, tab2, tab3 = st.tabs(["📈 Overview", "🔄 Returns Analysis", "💰 Revenue Analysis"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1: st.plotly_chart(plot_return_rate(filtered_df), use_container_width=True)
        with col2: st.plotly_chart(plot_category_return_percentage(filtered_df), use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1: st.plotly_chart(plot_return_reason_pie(filtered_df), use_container_width=True)
        with col2: st.plotly_chart(plot_price_vs_days_scatter(filtered_df), use_container_width=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1: st.plotly_chart(plot_category_revenue_pie(filtered_df), use_container_width=True)
        with col2: st.plotly_chart(plot_revenue_histogram(filtered_df), use_container_width=True)
    
    # Data preview
    with st.expander(f"🔍 View Filtered Data ({len(filtered_df)} rows)"):
        st.dataframe(filtered_df)
    
    # Filter summary
    st.info(f"**Active Filters**: Category={selected_category}, Gender={selected_gender}, "
            f"Age={min_age}-{max_age}, Revenue=${min_revenue}-${max_revenue}, "
            f"Days={min_days}-{max_days}, Reasons={len(selected_reason)} selected")

if __name__ == "__main__":
    main()
 