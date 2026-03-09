import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.title("Data Entry Test Form")
st.write("Please fill out the fields. Data is saved directly to Google Sheets.")

# Establish the connection to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch existing data from "Sheet1" to make sure we don't overwrite it
# ttl=0 ensures we always get the freshest data
existing_data = conn.read(worksheet="Sheet1", usecols=list(range(3)), ttl=0)
existing_data = existing_data.dropna(how="all") # Clean up any empty rows

# Create the input form
with st.form("entry_form", clear_on_submit=True):
    name = st.text_input("Full Name *")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    email = st.text_input("Email Address *")
    
    submitted = st.form_submit_button("Submit Data")

    if submitted:
        if not name or not email:
            st.error("Validation Error: Name and Email are required fields.")
        elif "@" not in email or "." not in email:
            st.error("Validation Error: Please enter a valid email address.")
        else:
            # Format the new entry
            new_row = pd.DataFrame([{"Name": name, "Age": age, "Email": email}])
            
            try:
                # Combine old data with the new row
                updated_df = pd.concat([existing_data, new_row], ignore_index=True)
                
                # Push the updated data back to Google Sheets
                conn.update(worksheet="Sheet1", data=updated_df)
                
                st.success(f"Success! {name}'s data has been saved to Google Sheets.")
            except Exception as e:
                st.error(f"An error occurred: {e}")