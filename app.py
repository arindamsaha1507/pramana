"""Streamlit app for reference extraction."""

import streamlit as st
from reference import get_references  # Replace 'your_module' with the actual name of your module

def card(title, author, year, url, citation):
    """Helper function to display a card"""
    st.markdown(f"### {title}")
    st.markdown(f"- [Link]({url}) {author} ({year})")
    st.markdown(f"```\n{citation}\n```")

# Streamlit page configuration
st.set_page_config(page_title="Reference Extractor", layout="wide")

# Title
st.title("Reference Extractor")

# Input fields
query = st.text_input("Enter your query:", "")
limit = st.number_input("Limit of references:", min_value=1, max_value=100, value=20)

textbox = st.empty()

# Button to extract references
if st.button("Extract References"):
    if query:
        # Extract references
        try:
            references = get_references(query, limit)

            # Display each reference
            for ref in references:
                ref.get_citation()
                card(ref.title[0], ref.authors, ref.year, ref.url, ref.citation)

        except Exception as e: # pylint: disable=broad-except
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a query to extract references.")

# Additional Streamlit components can be added here as needed
