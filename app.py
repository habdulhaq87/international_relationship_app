import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(page_title="International Relationship App", layout="wide")

# Title and description
st.title("🌍 International Relationship App")
st.write("Build meaningful relationships across the globe! Use the filters to find individuals who share your interests, speak your language, or are from specific regions.")

# Simulated data
data = {
    "Name": ["Alex", "Maria", "Li Wei", "Amina", "John", "Hiro", "Fatima", "Carlos"],
    "Country": ["USA", "Spain", "China", "Kenya", "Canada", "Japan", "Morocco", "Argentina"],
    "Interests": [
        "Technology, Sports", "Music, Art", "Cooking, Movies", "Travel, Books",
        "Gaming, Fitness", "Anime, Technology", "Cooking, Travel", "Sports, Music"
    ],
    "Languages Spoken": [
        "English", "Spanish", "Mandarin", "Swahili, English", "English, French",
        "Japanese, English", "Arabic, French", "Spanish, English"
    ],
    "Age": [25, 30, 22, 28, 35, 24, 27, 32],
    "Availability": ["Evenings", "Mornings", "Weekends", "Weekdays", "Flexible", "Evenings", "Flexible", "Weekends"],
}

df = pd.DataFrame(data)

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

# Display filtered data
st.subheader("🎯 Matches Found")
if not filtered_data.empty:
    st.write(f"Found {len(filtered_data)} match(es):")
    for _, row in filtered_data.iterrows():
        st.markdown(f"""
        **Name**: {row["Name"]}  
        **Country**: {row["Country"]}  
        **Age**: {row["Age"]}  
        **Languages Spoken**: {row["Languages Spoken"]}  
        **Interests**: {row["Interests"]}  
        **Availability**: {row["Availability"]}  
        ---
        """)
else:
    st.write("No matches found. Try adjusting the filters.")

# Footer
st.markdown("---")
st.write("© 2024 International Relationship App - Bringing the world closer together 🌐")
