import streamlit as st
import pandas as pd

# Define the main function for the backend
def main():
    st.title("🛠️ Backend - Data Entry")
    st.write("This page allows you to add new user profiles to the database. Fill in the details below and click 'Submit'.")

    # Load the existing database
    DATABASE_FILE = "database.csv"

    try:
        df = pd.read_csv(DATABASE_FILE)
    except FileNotFoundError:
        st.error("The database.csv file was not found. A new file will be created upon data entry.")
        df = pd.DataFrame(columns=["Name", "Country", "Interests", "Languages Spoken", "Age", "Availability"])

    # Data entry form
    with st.form("data_entry_form"):
        st.header("Enter New User Details")
        name = st.text_input("Name")
        country = st.text_input("Country (e.g., USA, France)")
        interests = st.text_area("Interests (comma-separated, e.g., Cooking, Sports)")
        languages_spoken = st.text_area("Languages Spoken (comma-separated, e.g., English, Spanish)")
        age = st.number_input("Age", min_value=0, max_value=120, step=1)
        availability = st.selectbox("Availability", ["Mornings", "Evenings", "Weekends", "Weekdays", "Flexible"])
        submit_button = st.form_submit_button("Submit")

    # Handle form submission
    if submit_button:
        if name and country and interests and languages_spoken and age:
            # Append the new user data to the DataFrame
            new_entry = pd.DataFrame({
                "Name": [name],
                "Country": [country],
                "Interests": [interests],
                "Languages Spoken": [languages_spoken],
                "Age": [age],
                "Availability": [availability]
            })
            df = pd.concat([df, new_entry], ignore_index=True)
            
            # Save the updated database
            df.to_csv(DATABASE_FILE, index=False)
            
            st.success(f"New user '{name}' has been successfully added to the database!")
        else:
            st.error("Please fill in all fields before submitting.")

    # Display the updated database
    st.header("Current Database")
    st.dataframe(df)
