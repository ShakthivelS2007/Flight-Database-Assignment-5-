import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Page Configuration
st.set_page_config(page_title="Flight Delay EDA", layout="wide")
st.title("Flight Delay Exploratory Data Analysis (EDA)")
st.subheader("Student: Shakthi vel. S | Reg No: 2117250020398")

# 2. Load Data Function mapped to your CSV columns
@st.cache_data
def load_data():
    df = pd.read_csv("jan_2025_flights.csv") 
    # Convert the date column using the correct name found in your file
    df['FLIGHTDATE'] = pd.to_datetime(df['FLIGHTDATE'])
    return df

try:
    df = load_data()
    
    st.sidebar.header("Filter Options")
    # Using MARKETING_AIRLINE_NETWORK as the carrier column
    carrier_list = df['MARKETING_AIRLINE_NETWORK'].unique()
    selected_carrier = st.sidebar.multiselect("Select Airlines", carrier_list, default=carrier_list[:5])

    filtered_df = df[df['MARKETING_AIRLINE_NETWORK'].isin(selected_carrier)]

    # Metrics using the correct delay column name: DEPDELAY
    col1, col2, col3 = st.columns(3)
    col1.metric("Avg Departure Delay", f"{filtered_df['DEPDELAY'].mean():.2f} mins")
    col2.metric("Max Delay Found", f"{filtered_df['DEPDELAY'].max():.2f} mins")
    col3.metric("Total Flights Analyzed", len(filtered_df))

    # Visualization 1: Bar Chart
    st.write("### Average Delay by Airline Network")
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    sns.barplot(data=filtered_df, x='MARKETING_AIRLINE_NETWORK', y='DEPDELAY', ax=ax1, palette="magma")
    plt.xticks(rotation=45)
    st.pyplot(fig1)

    # Visualization 2: Heatmap
    st.write("### Delay Heatmap (Day of Week vs Airline)")
    # Extract day name from FLIGHTDATE
    pivot_table = filtered_df.pivot_table(index='MARKETING_AIRLINE_NETWORK', 
                                         columns=filtered_df['FLIGHTDATE'].dt.day_name(), 
                                         values='DEPDELAY', 
                                         aggfunc='mean')
    
    # Reorder columns to be in chronological order
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot_table = pivot_table.reindex(columns=[d for d in days if d in pivot_table.columns])

    fig2, ax2 = plt.subplots(figsize=(12, 6))
    sns.heatmap(pivot_table, annot=True, cmap="YlOrRd", ax=ax2)
    st.pyplot(fig2)

except Exception as e:
    st.error(f"Error loading dashboard: {e}")
