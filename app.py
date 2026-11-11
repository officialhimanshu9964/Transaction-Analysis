import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu
from dataset import A
from pages_code.overview import showoverview
from pages_code.customer import showcustomer
from pages_code.detail import sector
from pages_code.transaction import transaction_trends
from pages_code.online import online_analysis
from pages_code.offline import offline_analysis
from pages_code.card import card_analysis
from pages_code.risk import showrisk
from pages_code.merchant import showmerchant
from pages_code.buisness import buisness


st.set_page_config(
    page_title="Transaction Intelligence",
    page_icon="📊",
    layout="wide"
)
st.markdown("""
<style>
.block-container {
    padding-top: 2.2rem !important;
}

section[data-testid="stSidebar"] > div {
    padding-top: 0rem !important;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:

    st.markdown("""
        <div style="padding: 0px; margin-top: -15px;">
            <h2 style="color:#F8FAFC; margin:0;">
                ◈ TRANS<span style="color:#38BDF8;">ACT</span>
            </h2>
            <p style="color:#64748B; font-size:12px;">
                FINANCIAL INTELLIGENCE PLATFORM
            </p>
        </div>
    """, unsafe_allow_html=True)

    page = option_menu(
        menu_title="WORKSPACE",
        options=[
            "Overview",
            "Transaction Trends",
            "Online Transactions",
            "Offline Transactions",
            "Customer Analysis",
            "Card Analysis",
            "Detail Analysis",
            "Merchant Analysis",
            "Risk Analysis",
            "Buisness Insigts"
        ],
        icons=[
            "grid-1x2",
            "graph-up",
            "globe",
            "shop",
            "people",
            "credit-card",
            "building",
            "shop-window",
            "shield-check",
            "graph-up"
        ],
        menu_icon="layers",
        default_index=0,
        styles={
            "container": {
                "background-color": "#0B1220",
                "padding": "8px",
                "border-radius": "12px"
            },
            "icon": {
                "color": "#94A3B8",
                "font-size": "15px"
            },
            "nav-link": {
                "color": "#94A3B8",
                "font-size": "13px",
                "text-align": "left",
                "margin": "3px",
                "padding": "10px 12px",
                "border-radius": "8px"
            },
            "nav-link-selected": {
                "background-color": "#172B46",
                "color": "#38BDF8",
                "font-weight": "600"
            }
        }
    )

    st.markdown("""
        <style>
        .block-container {
            padding-top: 2.2rem !important;
        }
        </style>
        <style>
             section[data-testid="stSidebar"] > div {
                 padding-top: 0rem !important;
             }
        </style>   
        <div style="
            position:relative;
            margin-top:35px;
            padding:14px;
            background:#111C2E;
            border-radius:10px;
            border:1px solid #1E293B;">
            <span style="color:#64748B;font-size:10px;">
                SYSTEM STATUS
            </span>
            <div style="color:#34D399;font-size:12px;margin-top:8px;">
                ● ANALYTICS ENGINE ONLINE
            </div>
        </div>
    """, unsafe_allow_html=True)


# MAIN CONTENT
if page == "Overview":
    showoverview()

elif page == "Transaction Trends":
    st.title("Transaction Trends")
    transaction_trends(A)

elif page == "Online Transactions":
    st.title("Online Transaction Analysis")
    online_analysis(A)

elif page == "Offline Transactions":
    st.title("Offline Transaction Analysis")
    offline_analysis(A)

elif page == "Customer Analysis":
    st.title("Customer Analysis")
    showcustomer()

elif page == "Card Analysis":
    st.title("Card Analysis")
    card_analysis(A)

elif page == "Detail Analysis":
    st.title("Detailed Analysis")
    sector()

elif page == "Merchant Analysis":
    st.title("Merchant Analysis")
    showmerchant()

elif page == "Risk Analysis":
    st.title("Risk & Anomaly Analysis")
    showrisk()

elif page == "Buisness Insigts":
    buisness()
