
import streamlit as st
import pandas as pd
import plotly.express as px
from dataset import A

def online_analysis(A):

    st.subheader("🌐 Online Transaction Analysis")

    df = A[["date", "amount", "transaction_id", "use_chip"]].copy()

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    df.dropna(subset=["amount", "use_chip"], inplace=True)

    online = df[df["use_chip"] == "Online Transaction"]

    total_transactions = len(df)
    online_transactions = len(online)

    online_amount = online["amount"].sum()

    online_percentage = (
        online_transactions / total_transactions * 100
        if total_transactions > 0 else 0
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Online Transactions",
        f"{online_transactions:,}"
    )

    col2.metric(
        "Online Transaction Amount",
        f"${online_amount:,.2f}"
    )

    col3.metric(
        "Online Transaction %",
        f"{online_percentage:.2f}%"
    )

    st.divider()

    with st.container(border=True):

        col1, col2 = st.columns(2)

        with col1:
            chart_type = st.selectbox(
                "Select Chart Type",
                ["Bar Chart", "Pie Chart", "Line Chart"],
                key="online_chart_type"
            )

        with col2:
            analysis = st.selectbox(
                "Select Analysis",
                [
                    "Transaction Count",
                    "Total Transaction Amount",
                    "Average Transaction Amount"
                ],
                key="online_analysis_type"
            )

        if st.button("Generate Analysis", type="primary"):

            channel_data = df.groupby("use_chip").agg(
                transaction_count=("transaction_id", "count"),
                total_amount=("amount", "sum"),
                avg_amount=("amount", "mean")
            ).reset_index()

            y_mapping = {
                "Transaction Count": "transaction_count",
                "Total Transaction Amount": "total_amount",
                "Average Transaction Amount": "avg_amount"
            }

            y = y_mapping[analysis]

            if chart_type == "Bar Chart":

                fig = px.bar(
                    channel_data,
                    x="use_chip",
                    y=y,
                    title=analysis
                )

            elif chart_type == "Pie Chart":

                fig = px.pie(
                    channel_data,
                    names="use_chip",
                    values=y,
                    title=analysis
                )

            else:

                fig = px.line(
                    channel_data,
                    x="use_chip",
                    y=y,
                    markers=True,
                    title=analysis
                )

            fig.update_layout(
                template="plotly_white",
                height=500,
                xaxis_title="Transaction Channel",
                yaxis_title=analysis
            )

            st.plotly_chart(fig, use_container_width=True)

        with st.expander("View Channel Summary"):

            st.dataframe(
                df.groupby("use_chip").agg(
                    transaction_count=("transaction_id", "count"),
                    total_amount=("amount", "sum"),
                    avg_amount=("amount", "mean")
                ).reset_index(),
                use_container_width=True,
                hide_index=True
            )


online_analysis(A)
