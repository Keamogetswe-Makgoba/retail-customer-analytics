import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Retail Insights Dashboard", layout="wide")

st.title("🚀 Online Store Executive Dashboard")
st.markdown("Analyzing **R8.9M** in revenue and customer behavior.")


@st.cache_data 
def load_data():
    df = pd.read_csv('OnlineRetail.csv', encoding='ISO-8859-1')
    df.dropna(subset=['CustomerID'], inplace=True)
    df = df[df['Quantity'] > 0]
    df['TotalSales'] = df['Quantity'] * df['UnitPrice']
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['Hour'] = df['InvoiceDate'].dt.hour
    return df

df = load_data()


st.sidebar.header("Filter Data")
hour_filter = st.sidebar.slider("Select Hour Range", 0, 23, (8, 18))
filtered_df = df[(df['Hour'] >= hour_filter[0]) & (df['Hour'] <= hour_filter[1])]


col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"R{filtered_df['TotalSales'].sum():,.2f}")
col2.metric("Unique Customers", filtered_df['CustomerID'].nunique())
col3.metric("Avg Sale Value", f"R{filtered_df['TotalSales'].mean():.2f}")

st.subheader("Top Products by Revenue")
top_p = filtered_df.groupby('Description')['TotalSales'].sum().sort_values(ascending=False).head(10).reset_index()
fig_products = px.bar(top_p, x='TotalSales', y='Description', orientation='h', color='TotalSales')
st.plotly_chart(fig_products, use_container_width=True)

st.subheader("Peak Shopping Hours")
hourly = filtered_df.groupby('Hour')['InvoiceNo'].nunique().reset_index()
fig_hour = px.line(hourly, x='Hour', y='InvoiceNo', markers=True)
st.plotly_chart(fig_hour, use_container_width=True)