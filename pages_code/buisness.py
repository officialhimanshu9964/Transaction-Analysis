import streamlit as st

def buisness():

    st.title("💼 Business Intelligence")
    st.caption("Transaction Intelligence | Executive Insights")


    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Customer Focus", "Top 20%", "45% Spending")

    with c2:
        st.metric("Merchant Concentration", "Top 10", "31% Volume")

    with c3:
        st.metric("Night Transactions", "+20%", "Avg Ticket")

    st.markdown("---")

    st.subheader("🚀 Strategic Business Recommendations")

    st.info("👑 **Customer Retention**\n\nProtect the top 20% of customers, as they generate 45% of total spending.")

    st.warning("🌐 **Online Payment Optimization**\n\nImprove online checkout reliability and investigate its comparatively high failure rate.")

    st.success("💳 **Card Security Upgrade**\n\nEncourage chip-based transactions and reduce reliance on swipe-based payments.")

    st.info("📊 **Credit Risk Management**\n\nRebuild credit-limit rules around credit score and debt-to-income instead of income alone.")

    st.markdown("---")

    st.subheader("👥 Customer Intelligence")

    with st.container(border=True):
        st.markdown("""
        **📌 Customer Activity**
        
        Identified the top 5 customers based on transaction records.

        **📌 Age Distribution**

        Most customers fall approximately between 38–60 years.

        **📌 Spending Behavior**

        Middle-aged customers contribute significantly to total spending, while younger customers show higher average spending.

        **📌 Financial Distribution**

        Transaction amount and per-capita income are highly right-skewed.

        **📌 Credit Behavior**

        The 18–25 age group shows comparatively higher average credit scores.
        """)

    st.markdown("---")

    st.subheader("💳 Card Intelligence")

    with st.container(border=True):
        st.markdown("""
        **💳 Payment Preference**

        Debit cards dominate transaction volume, followed by credit and prepaid cards.

        **🏦 Card Brands**

        American Express, Discover, Mastercard, and Visa.

        **👩 Gender Insights**

        Female customers have slightly higher average credit limits and represent a larger customer population.

        **📱 Payment Channels**

        Offline transactions significantly outnumber online transactions.
        """)

    st.markdown("---")

    st.success("""
    ### 🎯 Executive Conclusion

    Focus on customer retention, payment reliability, 
    credit risk optimization, and digital transaction growth 
    to improve overall transaction performance.
    """)
