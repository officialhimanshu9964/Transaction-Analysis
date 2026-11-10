
import streamlit as st
import pandas as pd
import plotly.express as px
from dataset import A


def transaction_trends(A):

    st.subheader("📈 Transaction Trends")

    df = A[["date", "amount", "transaction_id"]].copy()

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    df = df.dropna(subset=["date", "amount"])

    min_date = df["date"].min().date()
    max_date = df["date"].max().date()

    with st.container(border=True):

        date_range = st.date_input(
            "Select Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            key="trend_date_range"
        )

        if len(date_range) == 2:

            start_date, end_date = date_range

            df = df[
                (df["date"].dt.date >= start_date) &
                (df["date"].dt.date <= end_date)
            ]

        daily = df.groupby(df["date"].dt.date).agg(
            total_amount=("amount", "sum"),
            transaction_count=("transaction_id", "count"),
            avg_amount=("amount", "mean"),
            max_amount=("amount", "max"),
            min_amount=("amount", "min")
        ).reset_index()


        daily.rename(
            columns={"date": "transaction_date"},
            inplace=True
        )

        daily["rolling_avg"] = daily["total_amount"].rolling(
            window=7, min_periods=1
        ).mean()

        total_transactions = df["transaction_id"].count()
        total_amount = df["amount"].sum()
        avg_transaction = df["amount"].mean()
        max_transaction = df["amount"].max()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Transactions", f"{total_transactions:,}")
        col2.metric("Total Amount", f"${total_amount:,.2f}")
        col3.metric("Average Transaction", f"${avg_transaction:,.2f}")
        col4.metric("Highest Transaction", f"${max_transaction:,.2f}")

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            chart_type = st.selectbox(
                "Select Chart Type",
                ["Line Chart", "Bar Chart", "Area Chart"],
                key="trend_chart_type"
            )

        with col2:
            metric = st.selectbox(
                "Select Analysis",
                [
                    "Total Transaction Amount",
                    "Transaction Count",
                    "Average Transaction Amount",
                    "Maximum Transaction Amount",
                    "Minimum Transaction Amount",
                    "7-Day Rolling Average"
                ],
                key="trend_metric"
            )

        if st.button("Generate Trend", type="primary"):

            y = {
                "Total Transaction Amount": "total_amount",
                "Transaction Count": "transaction_count",
                "Average Transaction Amount": "avg_amount",
                "Maximum Transaction Amount": "max_amount",
                "Minimum Transaction Amount": "min_amount",
                "7-Day Rolling Average": "rolling_avg"
            }[metric]

            if chart_type == "Line Chart":
                fig = px.line(
                    daily,
                    x="transaction_date",
                    y=y,
                    markers=True,
                    title=metric
                )

            elif chart_type == "Bar Chart":
                fig = px.bar(
                    daily,
                    x="transaction_date",
                    y=y,
                    title=metric
                )

            else:
                fig = px.area(
                    daily,
                    x="transaction_date",
                    y=y,
                    title=metric
                )

            fig.update_layout(
                template="plotly_white",
                height=500,
                xaxis_title="Transaction Date",
                yaxis_title=metric,
                hovermode="x unified"
            )

            st.plotly_chart(fig, use_container_width=True)

        with st.expander("View Daily Transaction Summary"):

            st.dataframe(
                daily,
                use_container_width=True,
                hide_index=True
            )


transaction_trends(A)
