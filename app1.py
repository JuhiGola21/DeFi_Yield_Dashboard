import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.title("🦙 DeFi Yield Dashboard")

# Load data from DefiLlama API
@st.cache_data
def load_data():
    url = "https://yields.llama.fi/pools"
    r = requests.get(url)
    return pd.DataFrame(r.json()["data"])

df = load_data()

# Show top 10 APY pools
st.subheader("📊 Top DeFi Yields")
top_pools = df[["project", "symbol", "chain", "apy"]].sort_values(by="apy", ascending=False).head(10)
top_pools["label"] = top_pools["project"] + " - " + top_pools["symbol"] + " (" + top_pools["chain"] + ")"
st.dataframe(top_pools[["label", "apy"]].rename(columns={"label": "Pool", "apy": "APY (%)"}))

# Show bar chart
fig, ax = plt.subplots()
ax.barh(top_pools["label"], top_pools["apy"])
ax.set_xlabel("APY (%)")
ax.set_title("Top 10 DeFi Pools by APY")
plt.gca().invert_yaxis()
st.pyplot(fig)
# 📈 Enhanced Yield Calculator
st.subheader("📈 Yield Calculator")

amount = st.number_input("Deposit Amount (USD)", min_value=0.0, value=1000.0)
days = st.slider("Days Invested", 1, 365, 30)

# Pool selection (from top_pools)
selected = st.selectbox("Choose a Pool", options=top_pools.to_dict(orient = "records"),
                        format_func=lambda x: f"{x['project']} - {x['symbol']} ({x['chain']})")

# Yield calculation functions
def simple_yield(amount, apy, days):
    return amount * (apy / 100) * (days / 365)

def compound_yield(amount, apy, days):
    daily_rate = apy / 100 / 365
    return amount * ((1 + daily_rate) ** days - 1)

# Calculate on button click
if st.button("Calculate Earnings"):
    apy = selected["apy"]
    earnings_simple = simple_yield(amount, apy, days)
    earnings_compound = compound_yield(amount, apy, days)
   
    st.markdown(f"""
    ### 📊 Results for `{selected["project"]} - {selected["symbol"]}` on {selected["chain"]}
    - **APY**: `{apy:.2f}%`
    - **Simple Earnings**: `${earnings_simple:.2f}`
    - **Compound Earnings (daily)**: `${earnings_compound:.2f}`
    """)
