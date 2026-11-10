
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from dataset import A

def showrisk():

    st.title("Risk Analysis")
    A['Risk_Score'] = 0
    A.loc[
        A['card_on_dark_web'].str.lower() == 'yes',
        'Risk_Score'
    ] += 30
    customer_avg = A.groupby('customer_id')['amount'].transform('mean')

    A.loc[
        A['amount'] > customer_avg,
        'Risk_Score'
    ] += 30

    A.loc[
        A['errors'].str.lower() != 'none',
        'Risk_Score'
    ] += 20

    A.loc[
        A['merchant_city'] == 'ONLINE',
        'Risk_Score'
    ] += 10

    A['Risk'] = np.where(
        A['Risk_Score'] >= 60, 'High Risk',
        np.where(
            A['Risk_Score'] >= 30,
            'Medium Risk',
            'Low Risk'
        )
    )

    high = (A['Risk'] == 'High Risk').sum()
    medium = (A['Risk'] == 'Medium Risk').sum()
    low = (A['Risk'] == 'Low Risk').sum()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        with st.container(border=True):
            st.metric("High Risk Transactions", f"{high:,}")

    with col2:
        with st.container(border=True):
            st.metric("Medium Risk Transactions", f"{medium:,}")

    with col3:
        with st.container(border=True):
            st.metric("Low Risk Transactions", f"{low:,}")

    with col4:
        with st.container(border=True):
            st.metric(
                "Average Risk Score",
                f"{A['Risk_Score'].mean():.2f}"
            )


    col1, col2 = st.columns(2)

    with col1:
        st.header("Risk Distribution")

        with st.container(border=True):

            risk_data = A['Risk'].value_counts().reset_index()
            risk_data.columns = ['Risk', 'Transactions']

            fig = px.pie(
                risk_data,
                names='Risk',
                values='Transactions',
                hole=0.4,
                title="Transaction Risk Distribution"
            )

            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.header("Risk by Transaction Method")

        with st.container(border=True):

            method_risk = A.groupby('use_chip')['Risk'].value_counts().reset_index()
            method_risk.columns = ['Method', 'Risk', 'Transactions']

            fig = px.bar(
                method_risk,
                x='Method',
                y='Transactions',
                color='Risk',
                barmode='group',
                title="Risk by Payment Method"
            )

            st.plotly_chart(fig, use_container_width=True)

    st.header("Customer Risk Analysis")

    with st.container(border=True):

        customer_risk = A.groupby('customer_id').agg(
            Risk_Score=('Risk_Score', 'mean'),
            Credit_Score=('credit_score', 'first'),
            Total_Debt=('total_debt', 'first'),
            Yearly_Income=('yearly_income', 'first')
        ).reset_index()

        fig = px.scatter(
            customer_risk,
            x='Credit_Score',
            y='Risk_Score',
            hover_data=['customer_id'],
            title="Credit Score vs Average Risk Score"
        )

        st.plotly_chart(fig, use_container_width=True)


    st.header("High Risk Transactions")

    with st.container(border=True):

        high_risk = A[A['Risk'] == 'High Risk']

        st.dataframe(
            high_risk[
                [
                    'transaction_id',
                    'customer_id',
                    'date',
                    'amount',
                    'use_chip',
                    'errors',
                    'card_on_dark_web',
                    'Risk_Score'
                ]
            ].head(100),
            use_container_width=True,
            hide_index=True
        )
