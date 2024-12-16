import streamlit as st
import json
import os

# Define the file where the data will be stored
DATA_FILE = "content_data.json"
NOTES_FILE = "notes_data.json"

# Initialize the JSON file if it doesn't exist
def initialize_data_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)
    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "w") as f:
            json.dump([], f)

# Load data from the JSON file
def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def load_notes():
    with open(NOTES_FILE, "r") as f:
        return json.load(f)

# Save data to the JSON file
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def save_notes(notes):
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=4)

# Form to add new data
def data_entry_page():
    st.title("Data Entry")

    # Load existing data
    data = load_data()

    # Input or select main category
    main_category_mode = st.radio("Main Category:", ["Select Existing", "Add New"])
    if main_category_mode == "Select Existing":
        main_category = st.selectbox("Select Main Category", options=["Select"] + list(data.keys()))
    else:
        main_category = st.text_input("Enter New Main Category")

    if main_category and main_category != "Select":
        # Input or select subcategory
        sub_category_mode = st.radio("Sub Category:", ["Select Existing", "Add New"])
        if sub_category_mode == "Select Existing" and main_category in data:
            sub_category = st.selectbox("Select Sub Category", options=["Select"] + list(data[main_category].keys()))
        else:
            sub_category = st.text_input("Enter New Sub Category")
    else:
        sub_category = ""

    if sub_category and sub_category != "Select":
        # Input or select author
        author_mode = st.radio("Author:", ["Select Existing", "Add New"])
        if author_mode == "Select Existing" and main_category in data and sub_category in data[main_category]:
            author = st.selectbox("Select Author", options=["Select"] + list(data[main_category][sub_category].keys()))
        else:
            author = st.text_input("Enter New Author")
    else:
        author = ""

    # Input the link
    link = st.text_input("Link")

    # Add entry
    if st.button("Add Entry"):
        if main_category and sub_category and author and link:
            # Initialize the JSON structure if needed
            if main_category not in data:
                data[main_category] = {}
            if sub_category not in data[main_category]:
                data[main_category][sub_category] = {}
            if author not in data[main_category][sub_category]:
                data[main_category][sub_category][author] = []
            
            # Add the link
            data[main_category][sub_category][author].append(link)
            save_data(data)
            st.success("Entry added successfully!")
        else:
            st.error("Please fill in all fields.")

# Query page
def query_page():
    st.title("Query Data")

    # Load existing data
    data = load_data()

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

# Page to delete an author
def delete_author_page():
    st.title("Delete Author")

    # Load existing data
    data = load_data()

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
                # Confirm and delete author
                if st.button("Delete Author"):
                    del data[main_category][sub_category][author]

                    # Remove subcategory if empty
                    if not data[main_category][sub_category]:
                        del data[main_category][sub_category]

                    # Remove main category if empty
                    if not data[main_category]:
                        del data[main_category]

                    save_data(data)
                    st.success(f"Author '{author}' deleted successfully!")

# Page to manage notes
def notes_page():
    st.title("Notes")

    # Load existing notes
    notes = load_notes()

    # Display existing notes
    if notes:
        st.subheader("Your Notes")
        for i, note in enumerate(notes):
            col1, col2 = st.columns([8, 2])
            with col1:
                st.write(f"{i + 1}. {note}")
            with col2:
                if st.button("Delete", key=f"delete_{i}"):
                    notes.pop(i)
                    save_notes(notes)
                    st.rerun()

    # Input field to add a new note
    new_note = st.text_input("Add a new note")

    if st.button("Save Note"):
        if new_note.strip():
            notes.append(new_note.strip())
            save_notes(notes)
            st.success("Note saved successfully!")
            st.rerun()
        else:
            st.error("Note cannot be empty.")

# Main Streamlit app
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Data Entry", "Query Data", "Delete Author", "Notes"])

    initialize_data_file()

    if page == "Data Entry":
        data_entry_page()
    elif page == "Query Data":
        query_page()
    elif page == "Delete Author":
        delete_author_page()
    elif page == "Notes":
        notes_page()

if __name__ == "__main__":
    main()
