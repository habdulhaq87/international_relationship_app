import streamlit as st
import pandas as pd
import pydeck as pdk

# Page configuration
st.set_page_config(page_title="International Relationship App", layout="wide")

# Title and description
st.title("🌍 International Relationship App")
st.write("Build meaningful relationships across the globe! Use the filters to find individuals who share your interests, speak your language, or are from specific regions.")

# Load data from the CSV file in the main repository
try:
    df = pd.read_csv("database.csv")
except FileNotFoundError:
    st.error("The database.csv file was not found in the repository. Please make sure it exists in the main directory.")
    st.stop()

# Geocode each country into latitude and longitude
country_coords = {
    "USA": [37.0902, -95.7129],
    "Spain": [40.4637, -3.7492],
    "China": [35.8617, 104.1954],
    "Kenya": [-1.286389, 36.817223],
    "Canada": [56.1304, -106.3468],
    "Japan": [36.2048, 138.2529],
    "Morocco": [31.7917, -7.0926],
    "Argentina": [-38.4161, -63.6167],
    "Germany": [51.1657, 10.4515],
    "Australia": [-25.2744, 133.7751],
    "Italy": [41.8719, 12.5674],
    "South Africa": [-30.5595, 22.9375],
    "Brazil": [-14.2350, -51.9253],
    "India": [20.5937, 78.9629],
    "Russia": [61.5240, 105.3188],
    "France": [46.6034, 1.8883],
    "South Korea": [35.9078, 127.7669],
    "Netherlands": [52.1326, 5.2913],
    "Nigeria": [9.0820, 8.6753],
    "UK": [55.3781, -3.4360],
    "Sweden": [60.1282, 18.6435],
    "Mexico": [23.6345, -102.5528],
    "Egypt": [26.8206, 30.8025],
    "Turkey": [38.9637, 35.2433],
}

df["Latitude"] = df["Country"].map(lambda x: country_coords[x][0] if x in country_coords else None)
df["Longitude"] = df["Country"].map(lambda x: country_coords[x][1] if x in country_coords else None)

# Sidebar inputs for filtering
st.sidebar.header("Find Your Match")
selected_country = st.sidebar.selectbox("Select Country", ["All"] + sorted(df["Country"].unique().tolist()))
selected_language = st.sidebar.multiselect("Select Languages Spoken", sorted(set(", ".join(df["Languages Spoken"]).split(", "))))
selected_interest = st.sidebar.text_input("Enter an Interest (optional)")
age_range = st.sidebar.slider("Select Age Range", min_value=min(df["Age"]), max_value=max(df["Age"]), value=(min(df["Age"]), max(df["Age"])))
availability = st.sidebar.multiselect("Select Availability", sorted(df["Availability"].unique()))

# Filter data
filtered_data = df.copy()

# Filter by country
if selected_country != "All":
    filtered_data = filtered_data[filtered_data["Country"] == selected_country]

# Filter by languages
if selected_language:
    filtered_data = filtered_data[
        filtered_data["Languages Spoken"].apply(lambda langs: any(lang.strip() in langs for lang in selected_language))
    ]

# Filter by interest
if selected_interest:
    filtered_data = filtered_data[filtered_data["Interests"].str.contains(selected_interest, case=False, na=False)]

# Filter by age
filtered_data = filtered_data[
    (filtered_data["Age"] >= age_range[0]) & (filtered_data["Age"] <= age_range[1])
]

# Filter by availability
if availability:
    filtered_data = filtered_data[filtered_data["Availability"].isin(availability)]

# Display the map of users at the top
st.subheader("🗺️ User Locations")
if not filtered_data.empty and filtered_data[["Latitude", "Longitude"]].notnull().all().any():
    # Create a pydeck map
    map_data = filtered_data[["Latitude", "Longitude", "Name"]].dropna()
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=pdk.ViewState(
            latitude=0,  # Center the map on the world
            longitude=0,
            zoom=1.5,
            pitch=0,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=map_data,
                get_position="[Longitude, Latitude]",
                get_radius=500000,
                get_fill_color=[0, 128, 255, 160],
                pickable=True,
            )
        ],
        tooltip={"text": "{Name}"}
    ))
else:
    st.write("No map data available for the selected filters.")

# Display filtered data below the map
st.subheader("🎯 Matches Found")
if not filtered_data.empty:
    st.write(f"Found {len(filtered_data)} match(es):")
    # Display each user profile as a styled card
    for _, row in filtered_data.iterrows():
        st.markdown(
            f"""
            <div style="border: 1px solid #ddd; border-radius: 10px; padding: 15px; margin: 10px 0; background-color: #f9f9f9;">
                <h4 style="margin-bottom: 5px; color: #4CAF50;">{row["Name"]} ({row["Age"]} years old)</h4>
                <p style="margin: 5px 0;"><strong>Country:</strong> {row["Country"]}</p>
                <p style="margin: 5px 0;"><strong>Languages Spoken:</strong> {row["Languages Spoken"]}</p>
                <p style="margin: 5px 0;"><strong>Interests:</strong> {row["Interests"]}</p>
                <p style="margin: 5px 0;"><strong>Availability:</strong> {row["Availability"]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    st.write("No matches found. Try adjusting the filters.")

# Footer
st.markdown("---")
st.write("© 2024 International Relationship App - Bringing the world closer together 🌐")
