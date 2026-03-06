import streamlit as st
import pandas as pd
import os

# Name of your local Excel file
FILE_NAME = "data_entry_results.xlsx"

st.title("Data Entry Test Form")
st.write("Please fill out the fields below. The data will be verified and saved locally.")

# Create the input form
with st.form("entry_form", clear_on_submit=True):
    # You can easily design your own input fields here
    name = st.text_input("Full Name *")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    email = st.text_input("Email Address *")
    
    # The submit button
    submitted = st.form_submit_button("Submit Data")

    if submitted:
        # --- Data Verification ---
        if not name or not email:
            st.error("Validation Error: Name and Email are required fields.")
        elif "@" not in email or "." not in email:
            st.error("Validation Error: Please enter a valid email address.")
        else:
            # --- Save to Excel ---
            # Format the new entry
            new_data = pd.DataFrame({
                "Name": [name], 
                "Age": [age], 
                "Email": [email]
            })
            
            try:
                # Check if the file already exists
                if os.path.exists(FILE_NAME):
                    # Read existing data and append the new row
                    existing_data = pd.read_excel(FILE_NAME)
                    updated_data = pd.concat([existing_data, new_data], ignore_index=True)
                    updated_data.to_excel(FILE_NAME, index=False)
                else:
                    # Create a new file if it doesn't exist
                    new_data.to_excel(FILE_NAME, index=False)
                    
                st.success(f"Success! {name}'s data has been saved to {FILE_NAME}.")
            except Exception as e:
                st.error(f"An error occurred while saving to Excel: {e}")