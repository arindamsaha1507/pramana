"""Streamlit app for reference extraction."""

import streamlit as st
from reference import (
    get_references,
)  # Replace 'your_module' with the actual name of your module


def card(title, author, year, url, citation, abstract):
    """Helper function to display a card"""
    st.markdown(f"### {title}")
    st.markdown(f"- [Link]({url}) {author} ({year})")
    if abstract != "":
        with st.expander("Abstract", expanded=False):
            st.write(abstract)
    st.markdown(f"```\n{citation}\n```")


# Streamlit page configuration
st.set_page_config(page_title="Reference Extractor", layout="wide")

# Title
st.title("Pramāṇa: Personal Reference and Article Management Application")

st.markdown(
    """
    This app extracts references from a query using the 
    [Crossref API](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) 
    and [Habanero](https://github.com/sckott/habanero) client.

    Simply enter a search query and click the button to extract references.
    """
)

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
                ref.get_abstract()
                card(
                    ref.title[0],
                    ref.authors,
                    ref.year,
                    ref.url,
                    ref.citation,
                    ref.abstract,
                )

        except Exception as e:  # pylint: disable=broad-except
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a query to extract references.")

# Additional Streamlit components can be added here as needed
