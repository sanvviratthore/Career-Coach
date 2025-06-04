import streamlit as st
import folium
from streamlit_folium import st_folium
import requests

# ▸ Azure Maps subscription key (keep visible per your request)
AZURE_MAPS_KEY = "3pdOV7PLWQOOLunAlvdKIlRGdj0g7qPG6UgsnkO19Ge0VjSEouafJQQJ99BFACYeBjFAfOwiAAAgAZMP49Wn"

# ---------------- Azure Maps helpers ---------------- #
def geocode_place(place: str):
    """Return (lat, lon, formatted_address) for a place string."""
    url = "https://atlas.microsoft.com/search/address/json"
    params = {
        "subscription-key": AZURE_MAPS_KEY,
        "api-version": "1.0",
        "query": place,
        "limit": 1
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    results = r.json().get("results", [])
    if results:
        pos = results[0]["position"]
        addr = results[0]["address"]["freeformAddress"]
        return pos["lat"], pos["lon"], addr
    return None, None, None


def search_job_locations(lat: float, lon: float, query: str = "job", limit: int = 10):
    """Return POIs for given query around lat/lon."""
    url = "https://atlas.microsoft.com/search/poi/json"
    params = {
        "subscription-key": AZURE_MAPS_KEY,
        "api-version": "1.0",
        "lat": lat,
        "lon": lon,
        "query": query,
        "radius": 25000,   # 25 km radius
        "limit": limit
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    return r.json().get("results", [])


# ---------------- Streamlit page ---------------- #
def run():
    st.title("🌍 Global Insights – Job Hot-Spots")

    st.markdown(
        "Select a place (**type a city** or **click** on the map) to discover nearby "
        "**job/industry POIs** using Azure Maps."
    )

    # --- Text input for city search
    city_query = st.text_input("🔎 Search another city (e.g., Bengaluru, London):", value="Delhi")

    # --- Geocode on button
    if st.button("Go to city"):
        lat, lon, addr = geocode_place(city_query)
        if lat is None:
            st.error("Place not found.")
            st.stop()
        st.session_state["center"] = (lat, lon, addr)

    # Initialise map center in session_state
    if "center" not in st.session_state:
        # Default to Delhi on first load
        st.session_state["center"] = (28.6139, 77.2090, "Delhi, India")

    center_lat, center_lon, center_addr = st.session_state["center"]

    # --- Folium map (returns click events)
    m = folium.Map(location=[center_lat, center_lon], zoom_start=12)
    folium.Marker([center_lat, center_lon], tooltip=center_addr, icon=folium.Icon(color="blue")).add_to(m)

    map_state = st_folium(m, width=700, height=450)

    # --- Handle user map click
    if map_state and map_state.get("last_clicked"):
        click_lat = map_state["last_clicked"]["lat"]
        click_lon = map_state["last_clicked"]["lng"]
        st.session_state["center"] = (click_lat, click_lon, f"Lat {click_lat:.3f}, Lon {click_lon:.3f}")
        center_lat, center_lon, center_addr = st.session_state["center"]

    # --- Fetch POIs around current center
    with st.spinner("Fetching nearby job centres…"):
        pois = search_job_locations(center_lat, center_lon)

    if not pois:
        st.info("No job-related POIs found within 25 km.")
        return

    st.markdown(f"### 📌 Job POIs near **{center_addr}**")

    # --- POI list & secondary map with pins
    poi_map = folium.Map(location=[center_lat, center_lon], zoom_start=12)
    for idx, poi in enumerate(pois, start=1):
        pos = poi["position"]
        name = poi["poi"]["name"]
        dist = poi.get("dist", 0) / 1000  # metres → km
        addr = poi["address"]["freeformAddress"]
        folium.Marker(
            [pos["lat"], pos["lon"]],
            tooltip=name,
            popup=f"{name}<br>{addr}<br>{dist:.1f} km away",
            icon=folium.Icon(color="red", icon="briefcase", prefix="fa")
        ).add_to(poi_map)

        st.markdown(f"**{idx}. {name}** – {addr} (_{dist:.1f} km_)")

    st_folium(poi_map, width=700, height=450)

# For standalone debugging
if __name__ == "__main__":
    run()

