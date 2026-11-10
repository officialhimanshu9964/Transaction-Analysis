import streamlit as st
import plotly.express as px
from dataset import A
from dataset import sample
df=sample
def sector():
    st.subheader("Customer Demographics")
    
    chart1, chart2 ,chart3= st.columns(3)
    
    with chart1:
        fig = px.line(
            sample,
            x="agegroups",
            y="median_credit_score",
            title="Average Credit Score By AgeGroup",
            labels={
                "Avg Credit Score": "Avg_credit_limt"
            }
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with chart2:
        fig = px.line(
            sample,
            x="agegroups",
            y="total_spending",
            title="Average Total Spending by Gender",
            labels={
                "Avg Credit Score": "Avg_credit_limt"
            }
        )

        st.plotly_chart(fig, use_container_width=True)
    with chart3:
        fig = px.bar(
            sample,
            x="agegroups",
            y="Yearly_avg_income",
            title="Average Yearly Income by AgeGroup",
            labels={
                "Avg Credit Score": "Avg_credit_limt"
            }
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.title('DYNAMIC GRAPHICAL ANALYSIS')

    with st.container(border=True):

        col1, col2 = st.columns(2)

        with col1:
            x = st.selectbox(
                "X",
                df.columns,
                index=None,
                key="x_axis"
            )

        with col2:
            y = st.selectbox(
                "Y",
                df.columns,
                index=None,
                key="y_axis"
            )

        chart_type = st.selectbox(
            "Select Visualization",
            ["Scatter Plot", "Line Chart", "Bar Chart", "Histogram"],
            index=None,
            key="chart_type"
        )

        if st.button("Generate Analysis", key="generate_analysis"):

            if x and y and chart_type:

                if chart_type == "Scatter Plot":
                    fig = px.scatter(df, x=x, y=y)

                elif chart_type == "Line Chart":
                    fig = px.line(df, x=x, y=y)

                elif chart_type == "Bar Chart":
                    fig = px.bar(df, x=x, y=y)

                elif chart_type == "Histogram":
                    fig = px.histogram(df, x=x)

                st.plotly_chart(fig, use_container_width=True)

            else:
                st.warning("Please select X, Y, and Visualization.")
    st.divider()
    st.title('Data Table')
    st.dataframe(sample)