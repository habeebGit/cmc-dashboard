import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import time

# Streamlit App Configuration
st.set_page_config(page_title="Crypto Dashboard", layout="wide")

# API Configuration
API_KEY = "d64dd6a6-598a-4185-9ada-fabb637427a3"  # Replace with your CoinMarketCap API Key
headers = {
    'X-CMC_PRO_API_KEY': API_KEY
}

base_url = "https://pro-api.coinmarketcap.com/v1/"

# Fetch cryptocurrency listings
@st.cache_data(ttl=300)
def fetch_data():
    url = base_url + "cryptocurrency/listings/latest"
    params = {'start': '1', 'limit': '100', 'convert': 'USD'}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return pd.DataFrame(data['data'])

# Load Data
crypto_data = fetch_data()

# Sidebar - Search Functionality
st.sidebar.header("Search Cryptocurrency")
search_coin = st.sidebar.text_input("Enter Coin Name", "Bitcoin")

# Filter data for the searched coin
filtered_data = crypto_data[crypto_data['name'].str.contains(search_coin, case=False)]

# Display Market Data
st.title('📈 Cryptocurrency Dashboard')
st.write(f"### Live Price Tracking & Market Capitalization Rankings")
st.dataframe(crypto_data[['name', 'symbol', 'quote']].head(20))

# Display Search Results
if not filtered_data.empty:
    st.write(f"### Search Results for: {search_coin}")
    st.dataframe(filtered_data[['name', 'symbol', 'quote']])
else:
    st.write("No results found.")

# Display Price Chart
st.write("### Price Chart")
crypto_name = st.selectbox('Select Cryptocurrency', crypto_data['name'].unique())

# Fetch Historical Data (for charts)
@st.cache_data(ttl=300)
def fetch_historical_data(symbol):
    url = base_url + f"cryptocurrency/quotes/latest"
    params = {'symbol': symbol, 'convert': 'USD'}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return data

symbol = crypto_data[crypto_data['name'] == crypto_name]['symbol'].values[0]

historical_data = fetch_historical_data(symbol)
price = historical_data['data'][symbol]['quote']['USD']['price']
st.write(f"Current Price of {crypto_name}: ${price}")

# Auto-refresh
st_autorefresh = st.sidebar.checkbox("Enable Auto-Refresh", value=True)
if st_autorefresh:
    time.sleep(10)
    st.session_state["refresh_trigger"] = time.time()  # Modifying session state to trigger a rerun

