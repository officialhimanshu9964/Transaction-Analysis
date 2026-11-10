
import streamlit as st
import plotly.express as px
from dataset import A


def showmerchant():

    st.title("Merchant Analysis")

    merchant = A.dropna(subset=["merchant_id"])

    offline = A[A["merchant_city"] != "ONLINE"]
    online = A[A["merchant_city"] == "ONLINE"]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        with st.container(border=True):
            st.metric(
                "Total Merchants",
                f"{merchant['merchant_id'].nunique():,}"
            )

    with col2:
        with st.container(border=True):
            st.metric(
                "Total Merchant Volume",
                f"${merchant['amount'].sum()/1000000:,.2f}M"
            )

    with col3:
        with st.container(border=True):
            st.metric(
                "Average Transaction",
                f"${merchant['amount'].mean():,.2f}"
            )

    with col4:
        with st.container(border=True):
            st.metric(
                "Total Transactions",
                f"{len(merchant):,}"
            )

    st.divider()

    st.subheader("Online vs Offline Analysis")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):

            st.markdown("### Offline Transactions")

            c1, c2 = st.columns(2)

            c1.metric("Transactions", f"{len(offline):,}")
            c2.metric("Total Amount", f"${offline['amount'].sum()/1000000:,.2f}M")

            c3, c4 = st.columns(2)

            c3.metric("Unique Merchants", f"{offline['merchant_id'].nunique():,}")
            c4.metric("Average Amount", f"${offline['amount'].mean():,.2f}")

    with col2:
        with st.container(border=True):

            st.markdown("### Online Transactions")

            c1, c2 = st.columns(2)

            c1.metric("Transactions", f"{len(online):,}")
            c2.metric("Total Amount", f"${online['amount'].sum()/1000000:,.2f}M")

            c3, c4 = st.columns(2)

            c3.metric("Unique Merchants", f"{online['merchant_id'].nunique():,}")
            c4.metric("Average Amount", f"${online['amount'].mean():,.2f}")

    st.divider()

    st.subheader("Top Performing Merchants")

    top_merchant = (
        merchant.groupby("merchant_id")["amount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    top_merchant["merchant_id"] = top_merchant["merchant_id"].astype(str)

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):

            fig = px.bar(
                top_merchant.sort_values("amount"),
                x="amount",
                y="merchant_id",
                orientation="h",
                title="Top 10 Merchants by Transaction Amount",
                labels={
                    "amount": "Total Transaction Amount ($)",
                    "merchant_id": "Merchant ID"
                }
            )

            st.plotly_chart(fig, use_container_width=True)

    with col2:
        with st.container(border=True):

            merchant_count = (
                merchant.groupby("merchant_id")["transaction_id"]
                .count()
                .sort_values(ascending=False)
                .head(10)
                .reset_index()
            )

            merchant_count["merchant_id"] = merchant_count["merchant_id"].astype(str)

            fig = px.bar(
                merchant_count.sort_values("transaction_id"),
                x="transaction_id",
                y="merchant_id",
                orientation="h",
                title="Top 10 Merchants by Transaction Count",
                labels={
                    "transaction_id": "Number of Transactions",
                    "merchant_id": "Merchant ID"
                }
            )

            st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Merchant Payment Analysis")

    payment = merchant.groupby("use_chip")["amount"].sum().reset_index()

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):

            fig = px.pie(
                payment,
                names="use_chip",
                values="amount",
                title="Transaction Amount by Payment Method",
                hole=0.5
            )

            st.plotly_chart(fig, use_container_width=True)

    with col2:
        with st.container(border=True):

            fig = px.bar(
                payment,
                x="use_chip",
                y="amount",
                color="use_chip",
                title="Payment Method Revenue",
                labels={
                    "use_chip": "Payment Method",
                    "amount": "Transaction Amount ($)"
                }
            )

            st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Merchant Location Analysis")

    city_data = (
        offline.groupby("merchant_city")
        .agg(
            Total_Amount=("amount", "sum"),
            Transactions=("transaction_id", "count"),
            Merchants=("merchant_id", "nunique")
        )
        .sort_values("Total_Amount", ascending=False)
        .head(10)
        .reset_index()
    )

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):

            fig = px.bar(
                city_data.sort_values("Total_Amount"),
                x="Total_Amount",
                y="merchant_city",
                orientation="h",
                title="Top 10 Cities by Transaction Amount",
                labels={
                    "Total_Amount": "Transaction Amount ($)",
                    "merchant_city": "Merchant City"
                }
            )

            st.plotly_chart(fig, use_container_width=True)

    with col2:
        with st.container(border=True):

            fig = px.bar(
                city_data.sort_values("Transactions"),
                x="Transactions",
                y="merchant_city",
                orientation="h",
                title="Top 10 Cities by Transaction Count",
                labels={
                    "Transactions": "Number of Transactions",
                    "merchant_city": "Merchant City"
                }
            )

            st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.title("Analyse Individual Merchant")

    merchant_ids = sorted(merchant["merchant_id"].unique())

    option = st.selectbox(
        "SELECT MERCHANT ID",
        merchant_ids
    )

    if st.button("Show Merchant"):

        B = merchant[merchant["merchant_id"] == option]

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Transactions", f"{len(B):,}")

        with col2:
            st.metric("Total Amount", f"${B['amount'].sum():,.2f}")

        with col3:
            st.metric("Average Transaction", f"${B['amount'].mean():,.2f}")

        with col4:
            st.metric("Unique Customers", f"{B['client_id'].nunique():,}")

        col1, col2 = st.columns(2)

        with col1:
            with st.container(border=True):

                method = B["use_chip"].value_counts().reset_index()

                fig = px.pie(
                    method,
                    names="use_chip",
                    values="count",
                    title="Merchant Payment Methods",
                    hole=0.5
                )

                st.plotly_chart(fig, use_container_width=True)

        with col2:
            with st.container(border=True):

                daily = B.groupby("date")["amount"].sum().reset_index()

                fig = px.line(
                    daily,
                    x="date",
                    y="amount",
                    title="Merchant Daily Transaction Trend",
                    labels={
                        "date": "Date",
                        "amount": "Transaction Amount ($)"
                    }
                )

                st.plotly_chart(fig, use_container_width=True)

        st.subheader("Merchant Transaction Records")

        st.dataframe(
            B[[
                "transaction_id",
                "date",
                "client_id",
                "amount",
                "use_chip",
                "merchant_city"
            ]].sort_values("date", ascending=False),
            use_container_width=True
        )
