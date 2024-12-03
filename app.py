import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(page_title="International Relationship App", layout="wide")

# Title and description
st.title("International Relationship App 🌍")
st.write("Connect with individuals from around the world to build relationships, exchange culture, and learn new languages!")

# Simulated data
data = {
    "Name": ["Alex", "Maria", "Li Wei", "Amina", "John"],
    "Country": ["USA", "Spain", "China", "Kenya", "Canada"],
    "Interests": ["Technology, Sports", "Music, Art", "Cooking, Movies", "Travel, Books", "Gaming, Fitness"],
    "Languages Spoken": ["English", "Spanish", "Mandarin", "Swahili, English", "English, French"],
}

df = pd.DataFrame(data)

# Sidebar inputs for filtering
st.sidebar.header("Find Your Match")
selected_country = st.sidebar.selectbox("Select Country", ["All"] + df["Country"].unique().tolist())
selected_interest = st.sidebar.text_input("Enter an Interest (optional)")

# Filter data
filtered_data = df.copy()

if selected_country != "All":
    filtered_data = filtered_data[filtered_data["Country"] == selected_country]

if selected_interest:
    filtered_data = filtered_data[filtered_data["Interests"].str.contains(selected_interest, case=False, na=False)]

# Display filtered data
st.subheader("Available Matches")
if not filtered_data.empty:
    st.dataframe(filtered_data)
else:
    st.write("No matches found. Try adjusting the filters.")

# Footer
st.markdown("---")
st.write("© 2024 International Relationship App - Bringing the world closer together 🌐")
