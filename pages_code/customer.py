
import streamlit as st
import plotly.express as px
from dataset import sample
from dataset import A
import plotly.express as px

def showcustomer():

    st.title("👥 Customer Analytics")

    female = A[A["gender"] == "Female"]
    male = A[A["gender"] == "Male"]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        with st.container(border=True):
            st.metric(
                "Total Customers",
                f"{A['customer_id'].nunique():,}"
            )

    with col2:
        with st.container(border=True):
            st.metric(
                "Average Age",
                f"{A['current_age'].mean():.1f} yrs"
            )

    with col3:
        with st.container(border=True):
            st.metric(
                "Avg Credit Limit",
                f"${A['credit_limit'].mean():,.0f}"
            )

    with col4:
        with st.container(border=True):
            st.metric(
                "Avg Yearly Income",
                f"${A['yearly_income'].mean():,.0f}"
            )

    st.divider()

    st.subheader("Gender Segmentation")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 👩 Female Customers")

        with st.container(border=True):
            c1, c2 = st.columns(2)

            c1.metric(
                "Customers",
                f"{female['customer_id'].nunique():,}"
            )

            c2.metric(
                "Average Age",
                f"{female['current_age'].mean():.1f} yrs"
            )

            c3, c4 = st.columns(2)

            c3.metric(
                "Avg Credit Limit",
                f"${female['credit_limit'].mean():,.0f}"
            )

            c4.metric(
                "Avg Credit Cards",
                f"{female['num_credit_cards'].mean():.1f}"
            )

    with col2:
        st.markdown("### 👨 Male Customers")

        with st.container(border=True):
            c1, c2 = st.columns(2)

            c1.metric(
                "Customers",
                f"{male['customer_id'].nunique():,}"
            )

            c2.metric(
                "Average Age",
                f"{male['current_age'].mean():.1f} yrs"
            )

            c3, c4 = st.columns(2)

            c3.metric(
                "Avg Credit Limit",
                f"${male['credit_limit'].mean():,.0f}"
            )

            c4.metric(
                "Avg Credit Cards",
                f"{male['num_credit_cards'].mean():.1f}"
            )

    st.divider()

    st.subheader("Customer Demographics")

    chart1, chart2 ,chart3= st.columns(3)

    with chart1:
        gender_count = A.groupby("gender")["customer_id"].nunique()

        fig = px.pie(
            values=gender_count.values,
            names=gender_count.index,
            hole=0.55,
            title="Customer Distribution by Gender"
        )

        st.plotly_chart(fig, use_container_width=True)

    with chart2:
        gender_age = A.groupby("gender")["current_age"].mean().reset_index()

        fig = px.bar(
            gender_age,
            x="gender",
            y="current_age",
            color="gender",
            title="Average Age by Gender",
            labels={
                "gender": "Gender",
                "current_age": "Average Age"
            }
        )

        st.plotly_chart(fig, use_container_width=True)
    with chart3:
                credit = female.groupby("customer_id")["amount"].sum().sort_values(ascending=False).head(5)
                
                fig = px.pie(
                    values=credit.values,
                    names=credit.index,
                    title="Top 5 Female Customers by Spending",
                    hole=0.45
                )
    
                st.plotly_chart(fig, use_container_width=True)

    st.subheader("Financial Profile Comparison")

    col1, col2,col3 = st.columns(3)

    with col1:
        credit = A.groupby("gender")["credit_limit"].mean().reset_index()

        fig = px.bar(
            credit,
            x="gender",
            y="credit_limit",
            color="gender",
            title="Average Credit Limit",
            labels={"credit_limit": "Credit Limit"}
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        cards = A.groupby("gender")["num_credit_cards"].mean().reset_index()

        fig = px.bar(
            cards,
            x="gender",
            y="num_credit_cards",
            color="gender",
            title="Average Credit Cards",
            labels={"num_credit_cards": "Number of Cards"}
        )

        st.plotly_chart(fig, use_container_width=True)

    with col3:
            credit = male.groupby("customer_id")["amount"].sum().sort_values(ascending=False).head(5)

            fig = px.pie(
                values=credit.values,
                names=credit.index,
                title="Top 5 Male Customers by Spending",
                hole=0.45
            )

            st.plotly_chart(fig, use_container_width=True)
    st.divider()

    st.title('Analyse As Per Customer_id 🙎')
    option = st.selectbox(
    "SELECT CUSTOMER ID", list(A['customer_id'].value_counts().index.sort_values()))
    if st.button("Show Customer"):
        B = A[A['customer_id'] == option]
        col1,col2=st.columns(2)
        with col1:
            with st.container(border=True):
                c1, c2 = st.columns(2)
                c1.metric(
                    "Amount Spent",
                    f"${B['amount'].sum():,.2f}"
                    )

                c2.metric(
                    "Credit Limit",
                    f"${B['credit_limit'].max():,.0f}"
                    )

                c3, c4 = st.columns(2)

                c3.metric(
                    "Credit Cards",
                    f"{B['num_credit_cards'].iloc[0]:,.0f} Cards"
                    )

                c4.metric(
                    "Total Debt Of Customer",
                    f"${float(B['total_debt'].max()):,.2f}"
                    )
        with col2:
            with st.container(border=True):
                c1, c2 = st.columns(2)

                c1.metric(
                    "Credit Score Of Customer",
                    f"{A[A['customer_id']==2.0]['credit_score'].max():,}"
                )

                c2.metric(
                    "Birth Year",
                    f"{B['birth_year'].max():.1f}"
                )

                c3, c4 = st.columns(2)

                c3.metric(
                    "Birth Month",
                    f"{male['birth_month'].max():,.0f}"
                )

                c4.metric(
                    "Gender",
                    f"{male['gender'].iloc[0]}"
                )

