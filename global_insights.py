import streamlit as st
import folium
from streamlit_folium import st_folium
import requests

AZURE_MAPS_SUBSCRIPTION_KEY = "3pdOV7PLWQOOLunAlvdKIlRGdj0g7qPG6UgsnkO19Ge0VjSEouafJQQJ99BFACYeBjFAfOwiAAAgAZMP49Wn"

def search_job_locations(query="job", lat=28.6139, lon=77.2090):
    url = f"https://atlas.microsoft.com/search/poi/json"
    params = {
        'subscription-key': AZURE_MAPS_SUBSCRIPTION_KEY,
        'api-version': '1.0',
        'query': query,
        'lat': lat,
        'lon': lon,
        'limit': 5
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        return []

def run():
    st.title("🌍 Global Insights")

    st.markdown("""
    Welcome to the **Global Insights** section, where we provide:

    - Industry trends and analytics powered by **Azure OpenAI** and **Machine Learning**.
    - Real geospatial insights with **Azure Maps**.
    - Smart resume and document analysis via **Azure Document Intelligence**.
    """)

    st.markdown("---")
    st.subheader("📈 Job Market Trends")
    st.info("Job market trend graphs will appear here once integrated.")

    st.markdown("---")
    st.subheader("🗺️ Geospatial Job Data (Live from Azure Maps)")

    st.write("Searching for job centers near Delhi...")

    job_locations = search_job_locations()

    m = folium.Map(location=[28.6139, 77.2090], zoom_start=10)

    for place in job_locations:
        position = place['position']
        poi_name = place['poi']['name']
        folium.Marker(
            [position['lat'], position['lon']],
            popup=poi_name
        ).add_to(m)

    st_folium(m, width=700, height=500)

    st.markdown("---")
    st.subheader("📄 Document Intelligence")
    st.info("Insights from resumes and job descriptions will appear here.")

    st.markdown("---")
    st.caption("Powered by Azure Maps, OpenAI, and more 🚀")

