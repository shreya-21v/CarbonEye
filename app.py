import streamlit as st
import pandas as pd
from src.prediction_engine import process_vehicle_data, process_industry_data

st.set_page_config(page_title="Carbon Emission Monitoring", layout="wide")

st.title("🌍 AI-Based Carbon Emission Monitoring Dashboard")

st.markdown("### Automated detection of high-emission vehicles and industries")

if st.button("Run Emission Analysis"):
    process_vehicle_data()
    process_industry_data()
    st.success("Analysis Completed Successfully!")

st.header("🚗 High Emission Vehicles")

try:
    vehicles = pd.read_csv('data/vehicle_results.csv')
    high_vehicles = vehicles[vehicles['Status'] == 'HIGH']
    def color_status(val):
        color = 'red' if val == 'HIGH' else 'green'
        return f'color: {color}; font-weight: bold'

    st.dataframe(
    vehicles[['vehicle_no', 'Predicted_CO2', 'Status']]
    .style.applymap(color_status, subset=['Status'])
)

except:
    st.warning("Run analysis to generate vehicle results.")

st.header("🏭 High Polluting Industries")

try:
    industries = pd.read_csv('data/industry_results.csv')
    high_industries = industries[industries['Status'] == 'HIGH']
    st.dataframe(
    industries[['Industry_Name', 'Predicted_CO2', 'Status']]
    .style.applymap(color_status, subset=['Status'])
)

except:
    st.warning("Run analysis to generate industry results.")

import matplotlib.pyplot as plt

st.header("📊 Top Polluters Visualization")

# Button to show graphs
if st.button("Show Pollution Graphs"):

    # --- Vehicle Bar Chart ---
    try:
        top_vehicles = vehicles.sort_values(by="Predicted_CO2", ascending=False).head(5)

        st.subheader("🚗 Top 5 High Emission Vehicles")

        fig1, ax1 = plt.subplots(figsize=(4,2.5))  
        ax1.bar(top_vehicles["vehicle_no"], top_vehicles["Predicted_CO2"])
        ax1.set_xlabel("Vehicle No")
        ax1.set_ylabel("CO₂")
        ax1.set_title("Top Polluting Vehicles")
        plt.xticks(rotation=30)
        st.pyplot(fig1, use_container_width=False) 
    except:
        st.warning("Vehicle data not available yet.")

    # --- Industry Bar Chart ---
    try:
        top_industries = industries.sort_values(by="Predicted_CO2", ascending=False).head(5)

        st.subheader("🏭 Top 5 High Polluting Industries")

        fig2, ax2 = plt.subplots(figsize=(4,2.5)) 
        ax2.bar(top_industries["Industry_Name"], top_industries["Predicted_CO2"])
        ax2.set_xlabel("Industry")
        ax2.set_ylabel("CO₂")
        ax2.set_title("Top Polluting Industries")
        plt.xticks(rotation=30)
        st.pyplot(fig2, use_container_width=False)
    except:
        st.warning("Industry data not available yet.")

st.header("📈 Emission Trend Analysis")

if st.button("Show Emission Trend"):

    try:
        # Simulated trend using vehicle predictions
        trend_data = vehicles[['vehicle_no', 'Predicted_CO2']].copy()
        trend_data['Index'] = range(1, len(trend_data)+1)

        fig3, ax3 = plt.subplots(figsize=(4,2.5))
        ax3.plot(trend_data['Index'], trend_data['Predicted_CO2'], marker='o')
        ax3.set_xlabel("Sample Index")
        ax3.set_ylabel("Predicted CO₂")
        ax3.set_title("Vehicle Emission Trend")
        st.pyplot(fig3, use_container_width=False)
    except:
        st.warning("Run emission analysis first.")

st.header("📁 Download Emission Reports")

try:
    with open("data/vehicle_results.csv", "rb") as file:
        st.download_button(
            label="Download Vehicle Emission Report",
            data=file,
            file_name="vehicle_emission_report.csv",
            mime="text/csv"
        )
except:
    st.warning("Vehicle report not available yet.")

try:
    with open("data/industry_results.csv", "rb") as file:
        st.download_button(
            label="Download Industry Emission Report",
            data=file,
            file_name="industry_emission_report.csv",
            mime="text/csv"
        )
except:
    st.warning("Industry report not available yet.")

import pydeck as pdk
import numpy as np

st.header("🌍 Pollution Zone Map")

if st.button("Show Pollution Map"):

    try:
        # Take only HIGH emitters
        map_vehicles = vehicles[vehicles['Status'] == 'HIGH'].copy()
        map_industries = industries[industries['Status'] == 'HIGH'].copy()

        # Add random coordinates (simulated locations)
        map_vehicles["lat"] = np.random.uniform(12.8, 13.2, size=len(map_vehicles))
        map_vehicles["lon"] = np.random.uniform(77.4, 77.8, size=len(map_vehicles))

        map_industries["lat"] = np.random.uniform(12.8, 13.2, size=len(map_industries))
        map_industries["lon"] = np.random.uniform(77.4, 77.8, size=len(map_industries))

        # Combine both
        map_data = pd.concat([
            map_vehicles[['lat','lon','Predicted_CO2']],
            map_industries[['lat','lon','Predicted_CO2']]
        ])

        layer = pdk.Layer(
            "ScatterplotLayer",
            data=map_data,
            get_position='[lon, lat]',
            get_color='[255, 0, 0, 160]',
            get_radius=500
        )

        view_state = pdk.ViewState(
            latitude=13.0,
            longitude=77.6,
            zoom=9,
            pitch=50
        )

        st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

    except:
        st.warning("Run emission analysis first.")

