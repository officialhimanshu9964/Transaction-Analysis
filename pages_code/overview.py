
import streamlit as st
import plotly.express as px
from dataset import A

def showoverview():

    TOP5 = A.groupby("customer_id")["amount"].sum().sort_values(
        ascending=False
    ).head(5)

    st.title("Executive Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        with st.container(border=True):
            st.metric(
                "Total Transaction Amount",
                f"${A['amount'].sum()/1000000:,.2f} Million",
                delta="2 Million"
            )

    with col2:
        with st.container(border=True):
            st.metric(
                "Number Of Customer",
                A["customer_id"].nunique(),
                delta=250
            )

    with col3:
        with st.container(border=True):
            st.metric(
                "Number Of Merchant",
                A["merchant_id"].nunique(),
                delta=2000
            )

    with col4:
        with st.container(border=True):
            st.metric(
                "Transactions Records",
                f"{len(A)/1000000:,.2f} Million",
                delta=200
            )

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.metric(
                "Average Transaction Amount",
                f"${A['amount'].mean():,.2f}"
            )

    with col2:
        with st.container(border=True):
            st.metric(
                "Online Transactions",
                f"${A[A['merchant_city']=='ONLINE']['amount'].sum()/1000000:,.2f} Million"
            )

    with col3:
        with st.container(border=True):
            st.metric(
                "Offline Transactions",
                f"${A[A['merchant_city']!='ONLINE']['amount'].sum()/1000000:,.2f} Million"
            )

    col1, col2 = st.columns(2)

    with col1:
        st.header("Customers Location")

        with st.container(border=True):

            locations = A[
                ["customer_id", "latitude", "longitude",
                 "current_age", "gender", "credit_score"]
            ].drop_duplicates("customer_id")

            locations = locations.dropna(subset=["latitude", "longitude"])

            fig = px.scatter_map(
                locations,
                lat="latitude",
                lon="longitude",
                color="gender",
                hover_data=[
                    "customer_id",
                    "current_age",
                    "gender",
                    "credit_score"
                ],
                zoom=3,
                height=500
            )

            fig.update_layout(
                map_style="carto-darkmatter",
                map_center={"lat": 37.5, "lon": -96},
                map_zoom=3,
                margin=dict(l=0, r=0, t=0, b=0)
            )

            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.header("TOP 5 Customerid")

        with st.container(border=True):

            fig1 = px.pie(
                TOP5.reset_index(),
                names="customer_id",
                values="amount",
                title="Top 5 Customers by Spending",
                hole=0.4
            )

            st.plotly_chart(fig1, use_container_width=True)
