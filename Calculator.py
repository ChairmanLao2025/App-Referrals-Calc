import streamlit as st

# Sidebar navigation
page = st.sidebar.selectbox("Choose a page", ["Calculator", "Definitions"])

if page == "Calculator":
    st.title("Referral CAC vs CLV Calculator (with Real Fees)")

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

    st.subheader("📆 Monthly Plan")
    st.write(f"Gross CLV: £{monthly_clv:.2f}  *(See 'Definitions' in the sidebar)*")
    st.write(f"Net Revenue After Fees: £{monthly_net_revenue:.2f}")
    st.write(f"Total Fees: £{monthly_total_fees:.2f}")
    st.write(f"CAC: £{monthly_cac:.2f}  *(See 'Definitions')*")
    st.write(f"CAC as % of Net Revenue: {monthly_cac_pct:.2f}%")
    st.write(f"Net Profit per User: £{monthly_profit:.2f}")

    st.subheader("📅 Annual Plan")
    st.write(f"Gross CLV: £{annual_price:.2f}  *(See 'Definitions')*")
    st.write(f"Net Revenue After Fees: £{annual_net_revenue:.2f}")
    st.write(f"Total Fees: £{annual_total_fees:.2f}")
    st.write(f"CAC: £{annual_cac:.2f}  *(See 'Definitions')*")
    st.write(f"CAC as % of Net Revenue: {annual_cac_pct:.2f}%")
    st.write(f"Net Profit per User: £{annual_profit:.2f}")

elif page == "Definitions":
    st.title("📖 Definitions")

    st.markdown("### CLV – *Customer Lifetime Value*")
    st.write("The total amount of revenue you can expect from a single customer during their time using your product or service.")

    st.markdown("### CAC – *Customer Acquisition Cost*")
    st.write("The total cost it takes to acquire a new customer. In your case, this might be a referral commission or paid ad spend.")

    st.markdown("### Net Revenue")
    st.write("The revenue after deducting platform fees (like Stripe and Uscreen).")

    st.markdown("### Net Profit per User")
    st.write("Net revenue minus the cost of acquisition (e.g., referral commission). This tells you how much you truly make per customer.")
