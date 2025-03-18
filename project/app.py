from mod.conn import get_conn, run_query

import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import plotly.express as px
import plotly.graph_objects as go
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="E-commerce Analytics Hub", layout="wide")
st.sidebar.title("📊 E-commerce Analytics Hub")
st.sidebar.write("Navigate through various dashboards for comprehensive insights.")

option = st.sidebar.selectbox("Select Analysis Section", ["Overview", "Sales Analytics", "Product Analytics", "Customer Insights", "Seller Performance", "Payment Insights"])

def load_data(query):
    return run_query(query)

def customize_table(df):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(enabled=True)
    gb.configure_side_bar()
    gb.configure_default_column(editable=False, groupable=True)
    grid_options = gb.build()
    return AgGrid(df, gridOptions=grid_options, theme="alpine")

if option == "Overview":
    st.title("📌 General Overview")
    query = '''SELECT COUNT(DISTINCT customer_id) as Customers, COUNT(DISTINCT order_id) as Orders, ROUND(SUM(total_price), 2) as Revenue FROM olist_orders_cleaned_dataset;'''
    overview_data = load_data(query).iloc[0]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Customers", overview_data['Customers'])
    with col2:
        st.metric("Total Orders", overview_data['Orders'])
    with col3:
        st.metric("Total Revenue (₹)", overview_data['Revenue'])
    
    # Revenue Trend Visualization
    query_trend = '''SELECT date(order_purchase_timestamp) as Order_Date, SUM(total_price) as Revenue FROM olist_orders_cleaned_dataset GROUP BY date(order_purchase_timestamp) ORDER BY date(order_purchase_timestamp) DESC LIMIT 30;'''
    trend_data = load_data(query_trend)
    fig = px.line(trend_data, x="Order_Date", y="Revenue", title="📈 Revenue Trend (Last 30 Days)", template="plotly_dark", markers=True)
    st.plotly_chart(fig, use_container_width=True)

if option == "Sales Analytics":
    st.title("📈 Sales Analytics")
    query = '''SELECT date(order_purchase_timestamp) as Order_Date, SUM(total_price) as Total_Revenue, COUNT(order_id) as Total_Orders FROM olist_orders_cleaned_dataset GROUP BY date(order_purchase_timestamp) ORDER BY date(order_purchase_timestamp) DESC LIMIT 30;'''
    sales_data = load_data(query)
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.line(sales_data, x="Order_Date", y="Total_Revenue", title="💰 Daily Revenue Trend", template="seaborn", markers=True)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.bar(sales_data, x="Order_Date", y="Total_Orders", title="📦 Daily Order Volume", template="seaborn", color="Total_Orders", color_continuous_scale="Blues")
        st.plotly_chart(fig, use_container_width=True)

if option == "Product Analytics":
    st.title("📦 Product Analytics")
    query = '''SELECT p.product_category AS Category, COUNT(f.product_id) AS Total_Sales, SUM(f.quantity) AS Total_Quantity, ROUND(SUM(f.product_price * f.quantity), 2) AS Revenue FROM fact_table f JOIN olist_products_cleaned_dataset p ON f.product_id = p.product_id GROUP BY p.product_category ORDER BY Revenue DESC LIMIT 10;'''
    product_data = load_data(query)
    
    customize_table(product_data)
    fig = px.bar(product_data, x="Category", y="Revenue", title="💰 Revenue by Product Category", text="Revenue", template="seaborn", color="Revenue", color_continuous_scale="purples")
    st.plotly_chart(fig, use_container_width=True)

if option == "Customer Insights":
    st.title("👤 Customer Insights")
    query = '''SELECT c.customer_state AS State, COUNT(o.order_id) AS Total_Orders, ROUND(SUM(o.total_price), 2) AS Total_Revenue FROM olist_orders_cleaned_dataset o JOIN olist_customers_cleaned_dataset c ON o.customer_id = c.customer_id GROUP BY c.customer_state ORDER BY Total_Revenue DESC LIMIT 10;'''
    customer_data = load_data(query)
    
    customize_table(customer_data)
    fig_pie = px.pie(customer_data, names='State', values='Total_Revenue', title='📊 Revenue Distribution by State', template='seaborn', hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

if option == "Seller Performance":
    st.title("🏆 Seller Performance")
    query = '''SELECT s.seller_id AS Seller_ID, s.seller_state AS Seller_State, COUNT(DISTINCT f.order_id) AS Total_Orders, SUM(f.quantity) AS Total_Products_Sold, ROUND(SUM(f.product_price * f.quantity), 2) AS Revenue FROM fact_table f JOIN olist_sellers_cleaned_dataset s ON f.seller_id = s.seller_id GROUP BY s.seller_id, s.seller_state ORDER BY Revenue DESC LIMIT 10;'''
    seller_data = load_data(query)
    
    customize_table(seller_data)
    fig_bar = px.bar(seller_data, x="Seller_ID", y="Revenue", title="💰 Revenue by Seller", text="Revenue", template="seaborn", color="Revenue", color_continuous_scale="Blues")
    st.plotly_chart(fig_bar, use_container_width=True)

if option == "Payment Insights":
    st.title("💳 Payment Insights")
    query = '''SELECT payment_type AS Payment_Method, COUNT(order_id) AS Total_Transactions, ROUND(SUM(total_price), 2) AS Total_Revenue FROM olist_orders_cleaned_dataset GROUP BY payment_type ORDER BY Total_Revenue DESC;'''
    payment_data = load_data(query)
    
    customize_table(payment_data)
    fig_bar = px.bar(payment_data, x="Payment_Method", y="Total_Transactions", title="📍 Transactions by Payment Method", template="seaborn", color="Total_Transactions", color_continuous_scale="oranges")
    st.plotly_chart(fig_bar, use_container_width=True)

    fig_pie = px.pie(payment_data, names='Payment_Method', values='Total_Revenue', title='📊 Revenue Contribution by Payment Method', template='seaborn', hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)
