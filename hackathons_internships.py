import streamlit as st

# Replace with your Azure Maps primary key
AZURE_MAPS_KEY = "3pdOV7PLWQOOLunAlvdKIlRGdj0g7qPG6UgsnkO19Ge0VjSEouafJQQJ99BFACYeBjFAfOwiAAAgAZMP49Wn"

def run():
    st.title("📅 Hackathons in India")
    st.markdown("Discover upcoming hackathons happening in India!")

    # Static Azure Maps image centered on India
    latitude = 20.5937
    longitude = 78.9629

    map_url = (
        f"https://atlas.microsoft.com/map/static/png"
        f"?subscription-key={AZURE_MAPS_KEY}"
        f"&api-version=1.0"
        f"&center={longitude},{latitude}"
        f"&zoom=4"
        f"&width=700&height=400"
    )
    st.image(map_url, caption="India Map")

    st.markdown("### 🚀 Upcoming Hackathons (India)")

    # Valid upcoming hackathons in India (manually sourced)
    hackathons = [
        {"name": "Smart India Hackathon 2025", "date": "July 2025", "url": "https://www.sih.gov.in/"},
        {"name": "Hack the Mountains 5.0", "date": "August 2025", "url": "https://hackthemountains.tech/"},
        {"name": "HackJNU 2025", "date": "September 2025", "url": "https://hackjnu.tech/"},
        {"name": "HackMol 5.0", "date": "October 2025", "url": "https://hackmol.tech/"},
        {"name": "HackNITR 4.0", "date": "December 2025", "url": "https://hacknitr.tech/"},
        {"name": "HackVSIT 2025", "date": "To Be Announced", "url": "https://hackvsit.tech/"},
        {"name": "TechSurf Hackathon", "date": "To Be Announced", "url": "https://techsurf.tech/"},
        {"name": "DevScript Winter of Code", "date": "Winter 2025", "url": "https://devscript.tech/woc"},
    ]

    for hack in hackathons:
        st.markdown(f"- **[{hack['name']}]({hack['url']})** – {hack['date']}")


