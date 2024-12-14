import streamlit as st
import json
import os

# Define the files where the data will be stored
DATA_FILE = "content_data.json"
NOTES_FILE = "notes_data.json"

# Initialize the JSON files if they don't exist
def initialize_files():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)
    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "w") as f:
            json.dump([], f)

# Load data from a JSON file
def load_data(file):
    with open(file, "r") as f:
        return json.load(f)

# Save data to a JSON file
def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# Form to add new data
def data_entry_page():
    st.title("Data Entry")

    # Load existing data
    data = load_data(DATA_FILE)

    # Input fields for data entry
    main_category = st.selectbox("Main Category (e.g., Courses, Digital Products)", options=["Select"] + list(data.keys()))

    if main_category != "Select":
        sub_category = st.selectbox("Sub Category (e.g., Digital Marketing, Crypto)", options=["Select"] + list(data[main_category].keys()))
    else:
        sub_category = ""

    if sub_category and sub_category != "Select":
        author = st.selectbox("Author Name", options=["Select"] + list(data[main_category][sub_category].keys()))
    else:
        author = ""

    link = st.text_input("Link")

    if st.button("Add Entry"):
        if main_category != "Select" and sub_category and sub_category != "Select" and author and link:
            # Add data to the JSON structure
            if main_category not in data:
                data[main_category] = {}
            if sub_category not in data[main_category]:
                data[main_category][sub_category] = {}
            if author not in data[main_category][sub_category]:
                data[main_category][sub_category][author] = []
            
            # Add the link
            data[main_category][sub_category][author].append(link)
            save_data(DATA_FILE, data)
            st.success("Entry added successfully!")
        else:
            st.error("Please fill in all fields.")

# Query page
def query_page():
    st.title("Query Data")

    # Load existing data
    data = load_data(DATA_FILE)

    if not data:
        st.warning("No data available. Please add some entries first.")
        return

    # Main category selection
    main_category = st.selectbox("Select Main Category", options=["Select"] + list(data.keys()))

    if main_category != "Select":
        # Subcategory selection
        sub_category = st.selectbox("Select Sub Category", options=["Select"] + list(data[main_category].keys()))

        if sub_category != "Select":
            # Author selection
            author = st.selectbox("Select Author", options=["Select"] + list(data[main_category][sub_category].keys()))

            if author != "Select":
                # Display links
                links = data[main_category][sub_category][author]
                st.write("Links:")
                for link in links:
                    st.write(f"- [Link]({link})")

# Delete author page
def delete_author_page():
    st.title("Delete Author")

    # Load existing data
    data = load_data(DATA_FILE)

    if not data:
        st.warning("No data available. Please add some entries first.")
        return

    # Main category selection
    main_category = st.selectbox("Select Main Category", options=["Select"] + list(data.keys()))

    if main_category != "Select":
        # Subcategory selection
        sub_category = st.selectbox("Select Sub Category", options=["Select"] + list(data[main_category].keys()))

        if sub_category != "Select":
            # Author selection
            author = st.selectbox("Select Author to Delete", options=["Select"] + list(data[main_category][sub_category].keys()))

            if author != "Select":
                if st.button("Delete Author"):
                    del data[main_category][sub_category][author]

                    # Clean up empty structures
                    if not data[main_category][sub_category]:
                        del data[main_category][sub_category]
                    if not data[main_category]:
                        del data[main_category]

                    save_data(DATA_FILE, data)
                    st.success(f"Author '{author}' deleted successfully!")

# Notes page
def notes_page():
    st.title("My Notes")

    # Load existing notes
    notes = load_data(NOTES_FILE)

    # Display existing notes with delete option
    if notes:
        st.subheader("Previous Notes:")
        for i, note in enumerate(notes):
            cols = st.columns([4, 1])
            cols[0].write(f"{i + 1}. {note}")
            if cols[1].button("Delete", key=f"delete_{i}"):
                notes.pop(i)
                save_data(NOTES_FILE, notes)
                st.success("Note deleted successfully!")
                st.rerun()

    # Input field to add a new note
    new_note = st.text_input("Add a new note")

    if st.button("Save Note"):
        if new_note:
            notes.append(new_note)
            save_data(NOTES_FILE, notes)
            st.success("Note added successfully!")
            st.rerun()
        else:
            st.error("Please enter a note before saving.")

# Main Streamlit app
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Data Entry", "Query Data", "Delete Author", "My Notes"])

    initialize_files()

    if page == "Data Entry":
        data_entry_page()
    elif page == "Query Data":
        query_page()
    elif page == "Delete Author":
        delete_author_page()
    elif page == "My Notes":
        notes_page()

if __name__ == "__main__":
    main()
