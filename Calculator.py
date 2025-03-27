import streamlit as st

st.title("Referral CAC vs CLV Calculator (with Fees)")

st.header("Platform Fees")
stripe_fee = st.number_input("Stripe Fee (%)", value=2.9)
uscreen_fee = st.number_input("Uscreen Fee (%)", value=10.0)
total_fee_pct = (stripe_fee + uscreen_fee) / 100

st.header("Monthly Plan Inputs")
monthly_price = st.number_input("Monthly Subscription Price (£)", value=12.99)
monthly_commission = st.number_input("Referral Commission on Monthly Plan (%)", value=30.0)
monthly_retention = st.number_input("Average Retention (months)", value=3)

st.header("Annual Plan Inputs")
annual_price = st.number_input("Annual Subscription Price (£)", value=129.99)
annual_commission = st.number_input("Referral Commission on Annual Plan (%)", value=30.0)

# Monthly calculations
monthly_clv = monthly_price * monthly_retention
monthly_revenue_after_fees = monthly_clv * (1 - total_fee_pct)
monthly_cac = (monthly_commission / 100) * monthly_price
monthly_profit = monthly_revenue_after_fees - monthly_cac
monthly_cac_pct = (monthly_cac / monthly_revenue_after_fees * 100) if monthly_revenue_after_fees else 0

# Annual calculations
annual_revenue_after_fees = annual_price * (1 - total_fee_pct)
annual_cac = (annual_commission / 100) * annual_price
annual_profit = annual_revenue_after_fees - annual_cac
annual_cac_pct = (annual_cac / annual_revenue_after_fees * 100) if annual_revenue_after_fees else 0

st.subheader("Monthly Plan")
st.write(f"Gross CLV: £{monthly_clv:.2f}")
st.write(f"CLV After Fees: £{monthly_revenue_after_fees:.2f}")
st.write(f"CAC: £{monthly_cac:.2f}")
st.write(f"CAC as % of Net Revenue: {monthly_cac_pct:.2f}%")
st.write(f"Net Profit per User: £{monthly_profit:.2f}")

st.subheader("Annual Plan")
st.write(f"Gross CLV: £{annual_price:.2f}")
st.write(f"CLV After Fees: £{annual_revenue_after_fees:.2f}")
st.write(f"CAC: £{annual_cac:.2f}")
st.write(f"CAC as % of Net Revenue: {annual_cac_pct:.2f}%")
st.write(f"Net Profit per User: £{annual_profit:.2f}")
