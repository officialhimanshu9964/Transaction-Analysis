import streamlit as st
import pandas as pd
import plotly.express as px
from dataset import A

def card_analysis(A):
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Unique Cards", f"{A['card_id'].nunique():,}")
    col2.metric("Total Transactions", f"{len(A):,}")
    col3.metric("Total Amount", f"${A['amount'].sum():,.2f}")
    col4.metric("Average Transaction", f"${A['amount'].mean():,.2f}")

    card_type = st.selectbox("Select Card Type", ["All"] + A["card_type"].dropna().unique().tolist())

    if card_type != "All":
        data = A[A["card_type"] == card_type]
    else:
        data = A.copy()

    analysis_type = st.selectbox(
        "Select Analysis",
        ["Transaction Count", "Total Amount", "Average Amount", "Card Brand", "Chip Usage"]
    )

    if analysis_type == "Transaction Count":
        chart_data = data.groupby("card_type")["transaction_id"].count().reset_index()
        chart_data.columns = ["card_type", "value"]
        fig = px.bar(chart_data, x="card_type", y="value", title="Transactions by Card Type")

    elif analysis_type == "Total Amount":
        chart_data = data.groupby("card_type")["amount"].sum().reset_index()
        chart_data.columns = ["card_type", "value"]
        fig = px.bar(chart_data, x="card_type", y="value", title="Total Spending by Card Type")

    elif analysis_type == "Average Amount":
        chart_data = data.groupby("card_type")["amount"].mean().reset_index()
        chart_data.columns = ["card_type", "value"]
        fig = px.bar(chart_data, x="card_type", y="value", title="Average Transaction by Card Type")

    elif analysis_type == "Card Brand":
        chart_data = data.groupby("card_brand")["transaction_id"].count().reset_index()
        chart_data.columns = ["card_brand", "value"]
        fig = px.pie(chart_data, names="card_brand", values="value", title="Transactions by Card Brand")

    else:
        chart_data = data.groupby("has_chip")["transaction_id"].count().reset_index()
        chart_data.columns = ["has_chip", "value"]
        fig = px.pie(chart_data, names="has_chip", values="value", title="Chip vs Non-Chip Transactions")

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Card Brand Summary")

    brand_summary = data.groupby("card_brand").agg(
        transaction_count=("transaction_id", "count"),
        total_amount=("amount", "sum"),
        avg_amount=("amount", "mean"),
        unique_cards=("card_id", "nunique")
    ).reset_index()

    st.dataframe(brand_summary, use_container_width=True)

    st.subheader("Card Type Summary")

    type_summary = data.groupby("card_type").agg(
        transaction_count=("transaction_id", "count"),
        total_amount=("amount", "sum"),
        avg_amount=("amount", "mean"),
        unique_cards=("card_id", "nunique")
    ).reset_index()

    st.dataframe(type_summary, use_container_width=True)