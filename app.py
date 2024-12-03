import streamlit as st
import pandas as pd
import pydeck as pdk
import backend  # Importing the backend module

# Page configuration
st.set_page_config(page_title="International Relationship App", layout="wide")

# Navigation between main app and backend
page = st.sidebar.selectbox("Navigate", ["Main App", "Data Entry (Backend)"])

if page == "Main App":
    # Title and description
    st.title("🌍 International Relationship App")
    st.write("Build meaningful relationships across the globe! Use the filters to find individuals who share your interests, speak your language, or are from specific regions.")

    # Load user data and country coordinates
    try:
        user_data = pd.read_csv("database.csv")
        country_data = pd.read_csv("country.csv")
    except FileNotFoundError as e:
        st.error(f"Error: {e}")
        st.stop()

    # Merge user data with country coordinates
    user_data = user_data.merge(country_data, on="Country", how="left")

    # Sidebar inputs for filtering
    st.sidebar.header("Find Your Match")
    selected_country = st.sidebar.selectbox("Select Country", ["All"] + sorted(user_data["Country"].unique().tolist()))
    selected_language = st.sidebar.multiselect("Select Languages Spoken", sorted(set(", ".join(user_data["Languages Spoken"]).split(", "))))
    selected_interest = st.sidebar.text_input("Enter an Interest (optional)")
    age_range = st.sidebar.slider("Select Age Range", min_value=min(user_data["Age"]), max_value=max(user_data["Age"]), value=(min(user_data["Age"]), max(user_data["Age"])))
    availability = st.sidebar.multiselect("Select Availability", sorted(user_data["Availability"].unique()))

    # Filter data
    filtered_data = user_data.copy()

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
    st.write("© 2024 International Relation
