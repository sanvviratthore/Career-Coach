import streamlit as st
import folium
from streamlit_folium import st_folium
import requests

azure_maps_key = st.secrets["azure_maps_key"]

def geocode_place(place: str):
    """Return (lat, lon, formatted_address) for a place string."""
    url = "https://atlas.microsoft.com/search/address/json"
    params = {
        "subscription-key": azure_maps_key,
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
        "subscription-key": azure_maps_key,
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


def run():
    st.markdown("""
    <style>
    /* Center the main block */
    .appview-container .main {
        display: flex;
        justify-content: center;
    }
    /* Container to restrict max width and center */
    .centered-container {
        max-width: 800px;
        width: 100%;
        margin: 0 auto;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("🌍 Global Insights – Job Hot-Spots")

    with st.container():
        st.markdown('<div class="centered-container">', unsafe_allow_html=True)

        st.markdown(
            "Select a place (**type a city** or **click** on the map) to discover nearby "
            "**job/industry POIs** using Azure Maps."
        )
        st.markdown("---")

        col1, col2 = st.columns([3,1])
        with col1:
            city_query = st.text_input("🔎 Search another city (e.g., Bengaluru, London):", value="Delhi")
        with col2:
            go_clicked = st.button("Go to city")

        if "center" not in st.session_state:
            st.session_state["center"] = (28.6139, 77.2090, "Delhi, India")

        if go_clicked:
            lat, lon, addr = geocode_place(city_query)
            if lat is None:
                st.error("Place not found.")
                st.stop()
            st.session_state["center"] = (lat, lon, addr)

        center_lat, center_lon, center_addr = st.session_state["center"]

        m = folium.Map(location=[center_lat, center_lon], zoom_start=12)
        folium.Marker([center_lat, center_lon], tooltip=center_addr, icon=folium.Icon(color="blue")).add_to(m)

        map_state = st_folium(m, width=700, height=450)

        if map_state and map_state.get("last_clicked"):
            click_lat = map_state["last_clicked"]["lat"]
            click_lon = map_state["last_clicked"]["lng"]
            st.session_state["center"] = (click_lat, click_lon, f"Lat {click_lat:.3f}, Lon {click_lon:.3f}")
            center_lat, center_lon, center_addr = st.session_state["center"]

        with st.spinner("Fetching nearby job centres…"):
            pois = search_job_locations(center_lat, center_lon)

        if not pois:
            st.info("No job-related POIs found within 25 km.")
            return

        st.markdown(f"### 📌 Job POIs near **{center_addr}**")
        st.markdown("---")

        poi_map = folium.Map(location=[center_lat, center_lon], zoom_start=12)
        for idx, poi in enumerate(pois, start=1):
            pos = poi["position"]
            name = poi["poi"]["name"]
            dist = poi.get("dist", 0) / 1000
            addr = poi["address"]["freeformAddress"]
            folium.Marker(
                [pos["lat"], pos["lon"]],
                tooltip=name,
                popup=f"{name}<br>{addr}<br>{dist:.1f} km away",
                icon=folium.Icon(color="red", icon="briefcase", prefix="fa")
            ).add_to(poi_map)

            st.markdown(f"**{idx}. {name}** – {addr} (_{dist:.1f} km_)")

        st_folium(poi_map, width=700, height=450)

        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    run()
