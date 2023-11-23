"""Streamlit app for reference extraction."""

import streamlit as st
from reference import get_references, Reference


def card(ref: Reference):
    """Helper function to display a card"""
    st.markdown(f"### {ref.title}")
    st.markdown(f"- [Link]({ref.url}) {ref.authors} ({ref.year})")
    if ref.abstract != "":
        with st.expander("Abstract", expanded=False):
            st.write(ref.abstract)
    st.markdown(f"```\n{ref.citation}\n```")


def main():
    """Main function"""

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
        Click on the copy button on the top right of each box 
        to copy the BibTeX citation to your clipboard.

        Note: This app is still in development and may not work as expected. 
        Any feedback is welcome!
        """
    )

    # Input fields
    query = st.text_input("Enter your query:", "")
    limit = st.number_input(
        "Limit of references:", min_value=1, max_value=100, value=20
    )

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
                    card(ref)

            except Exception as e:  # pylint: disable=broad-except
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a query to extract references.")


if __name__ == "__main__":
    main()
