import streamlit as st
from PIL import Image
import pandas as pd

# Page config
st.set_page_config(
    page_title="Referrals System Analysis",
    layout="wide"
)

# Inject dark styling + table formatting
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Inter&display=swap" rel="stylesheet">
    <style>
    body {
        background-color: #000000;
        font-family: 'Inter', sans-serif !important;
    }
    .stApp {
        background-color: #000000;
        color: white;
        font-family: 'Inter', sans-serif !important;
    }
    h1, h2, h3, h4, h5, h6, .stMarkdown, .st-bb, .st-c0, label, .stSelectbox,
    input, textarea, .css-1aumxhk, .dataframe, table, th, td {
        color: white !important;
        font-family: 'Inter', sans-serif !important;
    }
    input, textarea {
        background-color: #000000 !important;
        border: 1px solid white !important;
    }
    .block-container {
        padding-top: 2rem;
    }
    .dataframe {
        background-color: black;
        border: 1px solid white;
    }
    table {
        border-collapse: collapse;
        font-family: 'Inter', sans-serif !important;
    }
    th, td {
        border: 1px solid white !important;
        padding: 8px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)



# Logo
logo = Image.open("Breathpod.png")
st.image(logo, width=600)

# Title
st.title("REWARDFUL x BREATHPOD - Referrals System Analysis")

# Purpose block
with st.expander("💡 What is the purpose of this tool?"):
    st.write("""
        This tool is designed for the internal team at Breathpod to evaluate the health and sustainability of our **referral strategy**.

        - **Customer Acquisition Cost (CAC)** helps us understand how much we're spending to bring in a new user, particularly through our Rewardful commission structure.
        - **Customer Lifetime Value (CLV)** shows the total revenue we can expect from a user based on retention.
        - **CAC / CLV Ratio** helps us understand cost efficiency.
        - Factoring in Stripe and Uscreen fees ensures our metrics reflect **real-world margins**, not vanity numbers.

        We can use this tool to **test assumptions, plan campaigns, and make confident decisions** about how we scale Breathpod through word-of-mouth and self-marketing loops.
    """)

# Inputs
st.header("Platform Fees")
stripe_fee_pct = st.number_input("Stripe Fee (%)", value=1.5)
stripe_fixed_fee = st.number_input("Stripe Fixed Fee (£)", value=0.20)
uscreen_fee_pct = st.number_input("Uscreen Fee (%)", value=5.4)
total_fee_pct = (stripe_fee_pct + uscreen_fee_pct) / 100

st.header("Rewardful Referral Commission")
commission_pct = st.number_input("Referral Commission (%)", value=30.0)

st.header("Monthly Subscription Plan Inputs")
monthly_price = st.number_input("Monthly Subscription Price (£)", value=12.99)
monthly_retention = st.number_input("Average Retention (months)", value=3)

st.header("Annual Subscription Plan Inputs")
annual_price = st.number_input("Annual Subscription Price (£)", value=129.99)

# Monthly calculations
monthly_clv = monthly_price * monthly_retention
monthly_total_fees = (monthly_clv * total_fee_pct) + (stripe_fixed_fee * monthly_retention)
monthly_net_revenue = monthly_clv - monthly_total_fees
monthly_cac = (commission_pct / 100) * monthly_price
monthly_profit = monthly_net_revenue - monthly_cac
monthly_cac_pct = (monthly_cac / monthly_net_revenue * 100) if monthly_net_revenue else 0
monthly_cac_to_clv = (monthly_cac / monthly_net_revenue * 100) if monthly_net_revenue else 0

# Annual calculations
annual_total_fees = (annual_price * total_fee_pct) + stripe_fixed_fee
annual_net_revenue = annual_price - annual_total_fees
annual_cac = (commission_pct / 100) * annual_price
annual_profit = annual_net_revenue - annual_cac
annual_cac_pct = (annual_cac / annual_net_revenue * 100) if annual_net_revenue else 0
annual_cac_to_clv = (annual_cac / annual_net_revenue * 100) if annual_net_revenue else 0

# Plan Comparison Table
table_data = {
    "Metric": [
        "Gross CLV",
        "Net Revenue After Fees",
        "Total Fees",
        "CAC",
        "CAC as % of Net Revenue",
        "Net Profit per User",
        "CAC / Net CLV Ratio (%)"
    ],
    "Monthly Subscription Plan": [
        f"£{monthly_clv:.2f}",
        f"£{monthly_net_revenue:.2f}",
        f"£{monthly_total_fees:.2f}",
        f"£{monthly_cac:.2f}",
        f"{monthly_cac_pct:.2f}%",
        f"£{monthly_profit:.2f}",
        f"{monthly_cac_to_clv:.2f}%"
    ],
    "Annual Subscription Plan": [
        f"£{annual_price:.2f}",
        f"£{annual_net_revenue:.2f}",
        f"£{annual_total_fees:.2f}",
        f"£{annual_cac:.2f}",
        f"{annual_cac_pct:.2f}%",
        f"£{annual_profit:.2f}",
        f"{annual_cac_to_clv:.2f}%"
    ]
}

df = pd.DataFrame(table_data)
st.subheader("📊 Plan Comparison Table")
st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)

# Affiliate Impact Calculator
st.markdown("---")
st.subheader("🤝 Affiliate Impact Calculator")

active_subscribers = st.number_input("Current number of active subscribers", value=100)
active_affiliates = st.number_input("Current number of active affiliates", value=10)
monthly_referrals = st.number_input("Avg Monthly Referrals per Affiliate", value=2)
annual_referrals = st.number_input("Avg Annual Referrals per Affiliate", value=24)

total_monthly_referrals = active_affiliates * monthly_referrals
total_annual_referrals = active_affiliates * annual_referrals
avg_clv_per_user = (monthly_clv + annual_price) / 2
estimated_annual_revenue = total_annual_referrals * avg_clv_per_user

st.markdown(f"**Total Monthly Referrals:** {total_monthly_referrals}")
st.markdown(f"**Total Annual Referrals:** {total_annual_referrals}")
st.markdown(f"**Estimated Revenue from Referrals (Year):** £{estimated_annual_revenue:,.2f}")

# Definitions
st.markdown("---")
st.markdown("### 🔍 Definitions")

st.markdown("""
| Term | Definition |
|------|------------|
| **CLV** | Customer Lifetime Value – total revenue expected from a customer |
| **CAC** | Customer Acquisition Cost – the cost to gain a user (e.g. referral payout) |
| **Net Revenue** | Revenue after Stripe and Uscreen fees are deducted |
| **Net Profit per User** | Net revenue minus CAC – what you actually earn per customer |
| **CAC / CLV Ratio** | Percentage of CLV spent on acquiring the user – lower is better |
""")
