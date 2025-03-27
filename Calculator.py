import streamlit as st
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="Referrals System Analysis",
    layout="wide"
)

# Inject custom CSS
st.markdown("""
    <style>
    body {
        background-color: #000000;
    }
    .stApp {
        background-color: #000000;
        color: white;
    }
    h1, h2, h3, h4, h5, h6, .stMarkdown, .st-bb, .st-c0, label, .stSelectbox {
        color: white !important;
    }
    .css-1aumxhk {
        color: white !important;
    }
    input, textarea {
        background-color: #000000 !important;
        color: white !important;
        border: 1px solid #555 !important;
    }
    .block-container {
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Logo
logo = Image.open("Breathpod.png")
st.image(logo, width=150)

# Title
st.title("Referrals System Analysis")

# Purpose explainer
with st.expander("💡 What is the purpose of this tool?"):
    st.write("""
        This tool is designed for the internal team at Breathpod to evaluate the health and sustainability of our **referral strategy**.

        - **Customer Acquisition Cost (CAC)** helps us understand how much we're spending to bring in a new user, particularly through our 30% referral offer.
        - **Customer Lifetime Value (CLV)** shows the total revenue we can expect from a user based on retention.
        - The difference between CLV and CAC represents **true profitability**, especially once we deduct platform fees.
        - Factoring in Stripe and Uscreen fees ensures our metrics reflect **real-world margins**, not vanity numbers.

        We use this tool to **test assumptions, plan campaigns, and make confident decisions** about how we scale Breathpod through word-of-mouth and self-marketing loops.
    """)

# Inputs
st.header("Platform Fees")
stripe_fee_pct = st.number_input("Stripe Fee (%)", value=1.5)
stripe_fixed_fee = st.number_input("Stripe Fixed Fee (£)", value=0.20)
uscreen_fee_pct = st.number_input("Uscreen Fee (%)", value=5.4)
total_fee_pct = (stripe_fee_pct + uscreen_fee_pct) / 100

st.header("Monthly Plan Inputs")
monthly_price = st.number_input("Monthly Subscription Price (£)", value=12.99)
monthly_commission = st.number_input("Referral Commission on Monthly Plan (%)", value=30.0)
monthly_retention = st.number_input("Average Retention (months)", value=3)

st.header("Annual Plan Inputs")
annual_price = st.number_input("Annual Subscription Price (£)", value=129.99)
annual_commission = st.number_input("Referral Commission on Annual Plan (%)", value=30.0)

# Monthly calculations
monthly_clv = monthly_price * monthly_retention
monthly_total_fees = (monthly_clv * total_fee_pct) + (stripe_fixed_fee * monthly_retention)
monthly_net_revenue = monthly_clv - monthly_total_fees
monthly_cac = (monthly_commission / 100) * monthly_price
monthly_profit = monthly_net_revenue - monthly_cac
monthly_cac_pct = (monthly_cac / monthly_net_revenue * 100) if monthly_net_revenue else 0

# Annual calculations
annual_total_fees = (annual_price * total_fee_pct) + stripe_fixed_fee
annual_net_revenue = annual_price - annual_total_fees
annual_cac = (annual_commission / 100) * annual_price
annual_profit = annual_net_revenue - annual_cac
annual_cac_pct = (annual_cac / annual_net_revenue * 100) if annual_net_revenue else 0

# Output in columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("📆 Monthly Plan")
    st.write(f"Gross CLV: £{monthly_clv:.2f}")
    st.write(f"Net Revenue After Fees: £{monthly_net_revenue:.2f}")
    st.write(f"Total Fees: £{monthly_total_fees:.2f}")
    st.write(f"CAC: £{monthly_cac:.2f}")
    st.write(f"CAC as % of Net Revenue: {monthly_cac_pct:.2f}%")
    st.write(f"Net Profit per User: £{monthly_profit:.2f}")

with col2:
    st.subheader("📅 Annual Plan")
    st.write(f"Gross CLV: £{annual_price:.2f}")
    st.write(f"Net Revenue After Fees: £{annual_net_revenue:.2f}")
    st.write(f"Total Fees: £{annual_total_fees:.2f}")
    st.write(f"CAC: £{annual_cac:.2f}")
    st.write(f"CAC as % of Net Revenue: {annual_cac_pct:.2f}%")
    st.write(f"Net Profit per User: £{annual_profit:.2f}")

# Definitions table
st.markdown("---")
st.markdown("### 🔍 Definitions")

st.markdown("""
| Term | Definition |
|------|------------|
| **CLV** | Customer Lifetime Value – total revenue expected from a customer |
| **CAC** | Customer Acquisition Cost – the cost to gain a user (e.g. referral payout) |
| **Net Revenue** | Revenue after Stripe and Uscreen fees are deducted |
| **Net Profit per User** | Net revenue minus CAC – what you actually earn per customer |
""")
