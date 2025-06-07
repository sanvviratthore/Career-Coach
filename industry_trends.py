import streamlit as st
import requests
import folium
from openai import AzureOpenAI
from streamlit_folium import st_folium

azure_maps_key = st.secrets["azure_maps_key"]
azure_openai_endpoint = st.secrets["azure_openai_endpoint"]
azure_openai_api_key = st.secrets["azure_openai_api_key"]
azure_openai_deployment = st.secrets["azure_openai_deployment"]
azure_openai_api_version = st.secrets["azure_openai_api_version"]

client = AzureOpenAI(
    api_key=azure_openai_api_key,
    azure_endpoint=azure_openai_endpoint,
    api_version=azure_openai_api_version,
)

def search_place(query):
    url = (
        f"https://atlas.microsoft.com/search/address/json?"
        f"subscription-key={azure_maps_key}&api-version=1.0&query={query}"
    )
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        if data["results"]:
            top = data["results"][0]
            pos = top["position"]
            return pos["lat"], pos["lon"], top["address"]["freeformAddress"]
    return None, None, None

def get_industry_trends(lat, lon):
    prompt = (
        f"You are a market analyst. Provide a brief analysis of industry trends "
        f"in the area with latitude {lat} and longitude {lon}. "
        f"Include companies, tech, job market, opportunities."
    )
    response = client.chat.completions.create(
        model=azure_openai_deployment,
        messages=[
            {"role": "system", "content": "You are a helpful industry trends assistant."},
            {"role": "user", "content": prompt},
        ],
        max_completion_tokens=800,
        temperature=0.7,
    )
    return response.choices[0].message.content

def run():
    st.title("🌍 Industry Trends Explorer with Search & Click Map")

    if "lat" not in st.session_state:
        st.session_state.lat = 28.6139
    if "lon" not in st.session_state:
        st.session_state.lon = 77.2090
    if "address" not in st.session_state:
        st.session_state.address = "New Delhi, India"
    if "trends" not in st.session_state:
        st.session_state.trends = ""
    if "clicked" not in st.session_state:
        st.session_state.clicked = False

    place_search = st.text_input("Search for a place:", key="place_search_input")

    if place_search:
        lat, lon, address = search_place(place_search)
        if lat and lon:
            st.session_state.lat = lat
            st.session_state.lon = lon
            st.session_state.address = address
            st.session_state.clicked = True
        else:
            st.warning("Place not found, try another query.")

    m = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=12)

    if st.session_state.clicked:
        folium.Marker(
            location=[st.session_state.lat, st.session_state.lon],
            popup=st.session_state.address,
            tooltip="Selected location",
            icon=folium.Icon(color="red"),
        ).add_to(m)

    click_data = st_folium(m, height=500, width=700)

    if click_data and click_data.get("last_clicked"):
        clicked_lat = click_data["last_clicked"]["lat"]
        clicked_lon = click_data["last_clicked"]["lng"]
        st.session_state.lat = clicked_lat
        st.session_state.lon = clicked_lon
        st.session_state.address = f"Lat: {clicked_lat:.5f}, Lon: {clicked_lon:.5f}"
        st.session_state.clicked = True

    if st.button("Get Industry Trends"):
        if not st.session_state.clicked:
            st.warning("Please select a location by searching or clicking on the map.")
        else:
            with st.spinner("Fetching industry trends..."):
                try:
                    st.session_state.trends = get_industry_trends(
                        st.session_state.lat, st.session_state.lon
                    )
                except Exception as e:
                    st.error(f"Error: {e}")

    if st.session_state.trends:
        st.markdown(f"### 📈 Industry Trends near {st.session_state.address}")
        st.write(st.session_state.trends)

if __name__ == "__main__":
    run()
