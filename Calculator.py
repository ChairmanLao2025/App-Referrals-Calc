import streamlit as st
from PIL import Image
import pandas as pd
import json
import os

# ---------- Persistence Setup ----------
DEFAULTS_FILE = "saved_inputs.json"

def load_saved_inputs():
    if os.path.exists(DEFAULTS_FILE):
        with open(DEFAULTS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_inputs(data):
    with open(DEFAULTS_FILE, "w") as f:
        json.dump(data, f)

saved = load_saved_inputs()

# ---------- Streamlit Config + Styling ----------
st.set_page_config(page_title="Referrals System Analysis", layout="wide")

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
    div[data-baseweb="select"] {
        background-color: black !important;
        color: white !important;
        border: 1px solid white !important;
    }
    div[data-baseweb="select"] * {
        color: white !important;
        background-color: black !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Logo ----------
logo = Image.open("Breathpod.png")
st.image(logo, width=600)

# ---------- Title & Purpose ----------
st.title("REWARDFUL x BREATHPOD - Referrals System Analysis")

with st.expander("💡 What is the purpose of this tool?"):
    st.write("""
        This tool is designed to evaluate the health and sustainability of our **referral strategy**.

        - **Customer Acquisition Cost (CAC)** helps us understand how much we're spending to bring in a new user, particularly through our Rewardful commission structure.
        - **Customer Lifetime Value (CLV)** shows the total revenue we can expect from a user based on retention.
        - **Net CLV** is the CLV after platform fees (Stripe & Uscreen) are deducted.
        - **CAC / CLV Ratio** helps us understand cost efficiency.

        We can use this tool to **test assumptions, plan campaigns, and make confident decisions** about how we scale Breathpod through word-of-mouth and self-marketing loops.
    """)

# ---------- Inputs ----------
st.header("Platform Fees")
stripe_fee_pct = st.number_input("Stripe Fee (%)", value=saved.get("stripe_fee_pct", 1.5))
stripe_fixed_fee = st.number_input("Stripe Fixed Fee (£)", value=saved.get("stripe_fixed_fee", 0.20))
uscreen_fee_pct = st.number_input("Uscreen Fee (%)", value=saved.get("uscreen_fee_pct", 5.4))
total_fee_pct = (stripe_fee_pct + uscreen_fee_pct) / 100

st.header("Rewardful Referral Commission")
commission_pct = st.number_input("Referral Commission (%)", value=saved.get("commission_pct", 30.0))

st.header("Monthly Subscription Plan Inputs")
monthly_price = st.number_input("Monthly Subscription Price (£)", value=saved.get("monthly_price", 12.99))
monthly_retention = st.number_input("Average Retention (months)", value=saved.get("monthly_retention", 3))

st.header("Annual Subscription Plan Inputs")
annual_price = st.number_input("Annual Subscription Price (£)", value=saved.get("annual_price", 129.99))

# ---------- Monthly Calculations ----------
monthly_clv = monthly_price * monthly_retention
monthly_total_fees = (monthly_clv * total_fee_pct) + (stripe_fixed_fee * monthly_retention)
monthly_net_revenue = monthly_clv - monthly_total_fees
monthly_cac = (commission_pct / 100) * monthly_price
monthly_profit = monthly_net_revenue - monthly_cac
monthly_cac_pct = (monthly_cac / monthly_net_revenue * 100) if monthly_net_revenue else 0
monthly_cac_to_clv = (monthly_cac / monthly_clv * 100) if monthly_clv else 0

# ---------- Annual Calculations ----------
annual_total_fees = (annual_price * total_fee_pct) + stripe_fixed_fee
annual_net_revenue = annual_price - annual_total_fees
annual_cac = (commission_pct / 100) * annual_price
annual_profit = annual_net_revenue - annual_cac
annual_cac_pct = (annual_cac / annual_net_revenue * 100) if annual_net_revenue else 0
annual_cac_to_clv = (annual_cac / annual_price * 100) if annual_price else 0

# ---------- Plan Comparison Table ----------
table_data = {
    "Metric": [
        "Gross CLV",
        "Net CLV (After Fees)",
        "Total Fees",
        "CAC (Commission Payment to Affiliate)",
        "CAC as % of Net CLV",
        "Net Profit per User",
        "CAC / CLV Ratio (%)"
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

# ---------- Affiliate Impact Calculator ----------
st.markdown("---")
st.subheader("🤝 Affiliate Impact Calculator")

active_subscribers = st.number_input("Current number of active subscribers", value=saved.get("active_subscribers", 100))
active_affiliates = st.number_input("Current number of active affiliates", value=saved.get("active_affiliates", 10))
monthly_referrals = st.number_input("Avg Monthly Referrals per Affiliate", value=saved.get("monthly_referrals", 0.1))
annual_referrals = st.number_input("Avg Annual Referrals per Affiliate", value=saved.get("annual_referrals", 0.1))

total_monthly_referrals = active_affiliates * monthly_referrals
total_annual_referrals = active_affiliates * annual_referrals
avg_clv_per_user = (monthly_clv + annual_price) / 2
estimated_annual_revenue = total_annual_referrals * avg_clv_per_user

st.markdown(f"**Total Monthly Referrals:** {total_monthly_referrals}")
st.markdown(f"**Total Annual Referrals:** {total_annual_referrals}")
st.markdown(f"**Estimated Additional Revenue from Referrals (Year):** £{estimated_annual_revenue:,.2f}")

# ---------- Rewardful Plan & ROI ----------
st.markdown("### 🧾 Rewardful Plan & ROI")

rewardful_plan = st.selectbox(
    "Select your Rewardful plan",
    options=[
        "Starter (£46.80/month inc VAT)",
        "Growth (£94.80/month inc VAT)",
        "Enterprise (£142.80/month inc VAT)"
    ],
    index=["Starter (£46.80/month inc VAT)", "Growth (£94.80/month inc VAT)", "Enterprise (£142.80/month inc VAT)"].index(saved.get("rewardful_plan", "Starter (£46.80/month inc VAT)"))
)

plan_costs = {
    "Starter (£46.80/month inc VAT)": 46.80,
    "Growth (£94.80/month inc VAT)": 94.80,
    "Enterprise (£142.80/month inc VAT)": 142.80
}

monthly_rewardful_cost = plan_costs[rewardful_plan]
annual_rewardful_cost = monthly_rewardful_cost * 12
roi_percent = (estimated_annual_revenue / annual_rewardful_cost * 100) if annual_rewardful_cost else 0
affect_on_pnl = estimated_annual_revenue - annual_rewardful_cost

st.markdown(f"**Monthly Cost of Rewardful (inc VAT):** £{monthly_rewardful_cost:.2f}")
st.markdown(f"**Annual Cost of Rewardful (inc VAT):** £{annual_rewardful_cost:.2f}")
st.markdown(f"**ROI on using Rewardful:** {roi_percent:.2f}%")
st.markdown(f"**Affect on P&L (Annual Net Revenue Impact):** £{affect_on_pnl:,.2f}")

# ---------- Save Button ----------
if st.button("💾 Save These Inputs as Default"):
    to_save = {
        "stripe_fee_pct": stripe_fee_pct,
        "stripe_fixed_fee": stripe_fixed_fee,
        "uscreen_fee_pct": uscreen_fee_pct,
        "commission_pct": commission_pct,
        "monthly_price": monthly_price,
        "monthly_retention": monthly_retention,
        "annual_price": annual_price,
        "active_subscribers": active_subscribers,
        "active_affiliates": active_affiliates,
        "monthly_referrals": monthly_referrals,
        "annual_referrals": annual_referrals,
        "rewardful_plan": rewardful_plan
    }
    save_inputs(to_save)
    st.success("Inputs saved successfully!")

# ---------- Definitions ----------
st.markdown("---")
st.markdown("### 🔍 Definitions")
st.markdown("""
| Term | Definition |
|------|------------|
| **CLV** | Customer Lifetime Value – total revenue expected from a customer |
| **Net CLV** | CLV after platform fees (Stripe + Uscreen) are deducted |
| **CAC** | Customer Acquisition Cost – the cost to gain a user (e.g. referral payout) |
| **Net Profit per User** | Net CLV minus CAC – what you actually earn per customer |
| **CAC / CLV Ratio** | Percentage of CLV spent on acquiring the user – lower is better |
""")

# ---------- Closing Image ----------
st.markdown("---")
st.image("DSCF0709.jpg", use_container_width=True)
