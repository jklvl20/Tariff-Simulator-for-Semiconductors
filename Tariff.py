import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tariff Impact with Elasticity", layout="centered")

st.title("Semiconductor Tariff Impact Simulator")

# Constants
base_chip_cost = 100
target_margin_rate = 0.34
base_quantity = 125400000

# User Inputs
tariff_rate = st.slider("Select Tariff Rate (%)", 0, 100, 10, step=5)
strategy = st.radio("Pricing Strategy", ["Pass Tariff to Consumer", "Absorb Tariff (Fixed Price)"])


# Base values (0% tariff)
base_final_cost = base_chip_cost
base_price = base_final_cost * (1 + target_margin_rate)

# Tariff-adjusted values
tariff_amount = base_chip_cost * (tariff_rate / 100)
cost_with_tariff = base_chip_cost + tariff_amount
final_cost = cost_with_tariff

if strategy == "Pass Tariff to Consumer":
    consumer_price = final_cost * (1 + target_margin_rate)
else:
    consumer_price = base_price  # Hold price steady
manufacturer_margin = consumer_price - final_cost

# Price change
price_change_pct = (consumer_price - base_price) / base_price
quantity_demanded = base_quantity * (1-price_change_pct)
consumer_surplus_before = 0.5*(368.2164-base_price)*base_quantity
producer_surplus_before = 0.5*(base_price-53.3731)*base_quantity
consumer_surplus_after = 0.5*(368.2164-consumer_price)*quantity_demanded
producer_surplus_after = 0.5*(consumer_price-53.3731)*quantity_demanded
deadweight_loss = ((consumer_surplus_before+producer_surplus_before) -
                   (consumer_surplus_after+producer_surplus_after))
tariff_revenue = (final_cost-base_final_cost)*quantity_demanded
sector_gross_profit=quantity_demanded*(consumer_price-final_cost)

# Output
st.markdown(f"### Results at {tariff_rate}% Tariff — **{strategy}**")
st.write(f"- Tariff Cost: **${tariff_amount:.2f}**")
st.write(f"- Final Cost per Unit: **${final_cost:.2f}**")
st.write(f"- Consumer Price: **${consumer_price:.2f}**")
st.write(f"- Manufacturer Margin: **${manufacturer_margin:.2f}**")
st.write(f"- Estimated Demand: **{int(quantity_demanded):,} units**")
st.write(f"- Consumer Surplus Before **${consumer_surplus_before:.2f}**")
st.write(f"- Producer Surplus Before **${producer_surplus_before:.2f}**")
st.write(f"- Consumer Surplus After **${consumer_surplus_after:.2f}**")
st.write(f"- Producer Surplus After **${producer_surplus_after:.2f}**")
st.write(f"- Deadweight loss: **${deadweight_loss:.2f}**")
st.write(f"- Estimated Import Sector Gross Revenue: **${sector_gross_profit:.2f}**")
st.write(f"- Estimated Import Sector Gross Revenue: **${tariff_revenue:.2f}**")
# Plot over range of tariffs
tariff_range = list(range(0, 101, 5))
quantities = []

for rate in tariff_range:
    t_amount = base_chip_cost * (rate / 100)
    t_cost = base_chip_cost + t_amount
    t_final = t_cost

    if strategy == "Pass Tariff to Consumer":
        c_price = t_final * (1 + target_margin_rate)
    else:
        c_price = base_price

    p_change = (c_price - base_price) / base_price
    qty = base_quantity * (1-p_change)

    quantities.append(qty)

df = pd.DataFrame({
    "Tariff Rate (%)": tariff_range,
    "Demand (units)": quantities
})

st.line_chart(df.set_index("Tariff Rate (%)"))



