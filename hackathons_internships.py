import streamlit as st
import requests
from openai import AzureOpenAI

AZURE_OPENAI_API_KEY = "F8cvPQQ5iKHG8NUJY0GbhH4Zxhll5BJQUMOapCLVoDQ6xX9V70tYJQQJ99BFACHYHv6XJ3w3AAAAACOGaJVI"
AZURE_OPENAI_ENDPOINT = "https://sanvi-mbf58gtv-eastus2.cognitiveservices.azure.com/"
AZURE_OPENAI_MODEL = "gpt-4.1"  
AZURE_OPENAI_API_VERSION = "2024-12-01-preview"

client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=AZURE_OPENAI_API_VERSION,
)

AZURE_MAPS_KEY = "3pdOV7PLWQOOLunAlvdKIlRGdj0g7qPG6UgsnkO19Ge0VjSEouafJQQJ99BFACYeBjFAfOwiAAAgAZMP49Wn"
AZURE_MAPS_SEARCH_URL = "https://atlas.microsoft.com/search/address/json"

def geocode_location(location: str):
    """Use Azure Maps Search API to convert location text to lat/lon."""
    params = {
        "subscription-key": AZURE_MAPS_KEY,
        "api-version": "1.0",
        "query": location,
        "limit": 1,
    }
    resp = requests.get(AZURE_MAPS_SEARCH_URL, params=params)
    if resp.status_code == 200:
        results = resp.json().get("results")
        if results:
            pos = results[0]["position"]
            return pos["lat"], pos["lon"]
    return None, None

def get_hackathons_from_openai(location: str) -> str:
    prompt = f"""
    You are an expert hackathon organizer. Provide a list of the top upcoming hackathons near "{location}" in the year 2025 specially after May 2025 including name, approximate date, and a short link to their official website or registration page. Return as a markdown list.
    """
    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_completion_tokens=400,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

def run():
    st.title("📅 Hackathons Near You")

    location_input = st.text_input("Enter your location (city, region, or country):", value="India")

    if location_input:
        lat, lon = geocode_location(location_input)

        if lat is None or lon is None:
            st.error("Could not find the location. Please enter a valid location.")
            return

        st.markdown(f"### Map Centered on: {location_input} (Lat: {lat}, Lon: {lon})")
        map_url = (
            f"https://atlas.microsoft.com/map/static/png"
            f"?subscription-key={AZURE_MAPS_KEY}"
            f"&api-version=1.0"
            f"&center={lon},{lat}"
            f"&zoom=7"
            f"&width=700&height=400"
            f"&language=en-US"
        )
        st.image(map_url, caption=f"Map around {location_input}")

        if st.button("Get Hackathons"):
            with st.spinner("Fetching hackathons near you..."):
                hackathons_md = get_hackathons_from_openai(location_input)
                st.markdown(hackathons_md)

if __name__ == "__main__":
    run()
