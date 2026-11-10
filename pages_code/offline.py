import streamlit as st
import pandas as pd
import plotly.express as px
from dataset import A

def offline_analysis(A):
    offline = A[A["use_chip"].isin(["Chip Transaction", "Swipe Transaction"])]
    channel_data = A.groupby("use_chip").agg(
        transaction_count=("transaction_id", "count"),
        total_amount=("amount", "sum"),
        avg_amount=("amount", "mean")
    ).reset_index()

    offline_count = len(offline)
    offline_amount = offline["amount"].sum()
    offline_percentage = (offline_count / len(A)) * 100

    col1, col2, col3 = st.columns(3)

    col1.metric("Offline Transactions", f"{offline_count:,}")
    col2.metric("Offline Transaction Amount", f"${offline_amount:,.2f}")
    col3.metric("Offline Transaction Share", f"{offline_percentage:.2f}%")

    chart_type = st.selectbox("Select Chart Type", ["Bar", "Pie", "Line"])
    analysis_type = st.selectbox(
        "Select Analysis",
        ["Transaction Count", "Total Amount", "Average Amount"]
    )

    if analysis_type == "Transaction Count":
        y = "transaction_count"
    elif analysis_type == "Total Amount":
        y = "total_amount"
    else:
        y = "avg_amount"

    if st.button("Generate Offline Analysis"):
        if chart_type == "Bar":
            fig = px.bar(channel_data, x="use_chip", y=y, title=f"{analysis_type} by Transaction Type")
        elif chart_type == "Pie":
            fig = px.pie(channel_data, names="use_chip", values=y, title=f"{analysis_type} by Transaction Type")
        else:
            fig = px.line(channel_data, x="use_chip", y=y, title=f"{analysis_type} by Transaction Type")

        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Offline Transaction Summary")

    offline_summary = offline.groupby("use_chip").agg(
        transaction_count=("transaction_id", "count"),
        total_amount=("amount", "sum"),
        avg_amount=("amount", "mean"),
        max_amount=("amount", "max"),
        min_amount=("amount", "min")
    ).reset_index()

    st.dataframe(offline_summary, use_container_width=True)