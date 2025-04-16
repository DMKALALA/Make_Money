import streamlit as st
import plotly.express as px
import pandas as pd
from data_loader import load_transactions, load_budget_summary, get_available_months, export_transactions_to_csv

st.set_page_config(page_title="📊 My YNAB Dashboard", layout="wide")
st.title("📊 My Budget Dashboard")

# 📆 Month selector
months = get_available_months()
selected_month = st.selectbox("Select a month:", months, index=0)

# 🔄 Load data for selected month
transactions_df = load_transactions(selected_month)
budget_summary = load_budget_summary(selected_month)

# 📋 Summary cards
col1, col2, col3 = st.columns(3)
col1.metric("💰 To Be Budgeted", f"${budget_summary['to_be_budgeted']:,.2f}")
col2.metric("📥 Inflow", f"${budget_summary['inflow']:,.2f}")
col3.metric("📤 Outflow", f"${budget_summary['outflow']:,.2f}")

# 📊 Inflow vs Outflow Bar Chart
st.subheader("📊 Inflow vs Outflow")
flow_df = pd.DataFrame.from_dict({
    "Type": ["Inflow", "Outflow"],
    "Amount": [budget_summary["inflow"], budget_summary["outflow"]],
})
fig = px.bar(flow_df, x="Type", y="Amount", color="Type", text="Amount", title="Cash Flow Overview")
st.plotly_chart(fig, use_container_width=True)

# 🏷️ Top Categories Pie
st.subheader(f"🏷️ Top Spending Categories in {selected_month.strftime('%m/%y')}")

if not transactions_df.empty and 'amount' in transactions_df.columns:
    spending_df = transactions_df[transactions_df['amount'] < 0]
    
    category_filter = st.multiselect("Filter by category:", spending_df['category_name'].unique())
    if category_filter:
        spending_df = spending_df[spending_df['category_name'].isin(category_filter)]

    if not spending_df.empty and 'category_name' in spending_df.columns:
        top_cats = spending_df.groupby('category_name')['amount'].sum().abs().nlargest(5).reset_index()
        fig2 = px.pie(top_cats, names='category_name', values='amount', title="Top 5 Spending Categories")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No categorized spending data found for selected filters.")
else:
    st.info("No transaction data available for this month.")


# 💸 Savings vs Spending Line Chart
st.subheader("💸 Savings vs Spending")

if not transactions_df.empty:
    savings_df = transactions_df[transactions_df['amount'] > 0].copy()
    spending_df = transactions_df[transactions_df['amount'] < 0].copy()

    savings_df['Amount'] = savings_df['amount'].cumsum()
    savings_df['Type'] = "Savings/Income"

    spending_df['Amount'] = spending_df['amount'].cumsum()
    spending_df['Type'] = "Spending"

    vs_df = pd.concat([savings_df[['date', 'Amount', 'Type']], spending_df[['date', 'Amount', 'Type']]])
    vs_df.rename(columns={"date": "Date"}, inplace=True)
    vs_df.sort_values(by="Date", inplace=True)

    fig3 = px.line(vs_df, x="Date", y="Amount", color="Type", title="Spending vs Savings Over Time")
    st.plotly_chart(fig3, use_container_width=True)

    # 📈 Net Savings Progression
    st.subheader("📈 Net Savings Progression")
    net_df = transactions_df.copy()
    net_df['net'] = net_df['amount'].cumsum()
    net_df.rename(columns={'date': 'Date'}, inplace=True)
    fig4 = px.line(net_df, x='Date', y='net', title='Net Savings Over Time')
    st.plotly_chart(fig4, use_container_width=True)

    # 🗂️ Breakdown by Category Over Time
    st.subheader("🗂️ Category Spending Over Time")
    cat_df = transactions_df[transactions_df['amount'] < 0].copy()
    cat_df['amount'] = cat_df['amount'].abs()
    fig5 = px.line(cat_df, x='date', y='amount', color='category_name', title="Category Spending Over Time")
    st.plotly_chart(fig5, use_container_width=True)

    # 🕒 Time Granularity Filter
    st.subheader("🕒 Time Granularity")
    granularity = st.radio("View by:", options=['Daily', 'Weekly', 'Monthly'], horizontal=True)

    agg_df = transactions_df.copy()
    agg_df['date'] = pd.to_datetime(agg_df['date'])  # Ensure datetimelike

    if granularity == 'Weekly':
        agg_df['period'] = agg_df['date'].dt.to_period('W').apply(lambda r: r.start_time)
    elif granularity == 'Monthly':
        agg_df['period'] = agg_df['date'].dt.to_period('M').apply(lambda r: r.start_time)
    else:
        agg_df['period'] = agg_df['date']

    summary = agg_df.groupby(['period'])['amount'].sum().cumsum().reset_index()
    fig6 = px.line(summary, x='period', y='amount', title=f'Cumulative Net Savings ({granularity})')
    st.plotly_chart(fig6, use_container_width=True)
else:
    st.info("Not enough data for savings vs spending analysis.")



# 📤 Export Button
if st.button("📥 Export Transactions to CSV"):
    csv_file = export_transactions_to_csv(transactions_df)
    st.success(f"Transactions exported to {csv_file}")
