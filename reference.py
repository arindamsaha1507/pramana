"""Module to extract reference from a query"""

import re

from dataclasses import dataclass

import requests

from habanero import Crossref, cn


@dataclass
class Reference:
    """Class to store information about a reference"""

    title: str
    doi: str
    authors: str = ""
    year: str = ""
    url: str = ""
    citation: str = ""
    abstract: str = ""

    def __repr__(self):
        return f"{self.title} ({self.doi})"

    def get_citation(self, typ: str = "bibtex"):
        """Get citation from a reference"""
        string = cn.content_negotiation(ids=self.doi, format=typ)
        string = string.replace(", ", "\n")
        self.citation = string

    def get_abstract(self):
        """Get abstract from a reference"""
        r = requests.get(f"https://api.crossref.org/works/{self.doi}", timeout=5)
        try:
            self.abstract = remove_jats_tags(r.json()["message"]["abstract"])
            print(self.abstract)
        except KeyError:
            self.abstract = ""
            # print(json.dumps(r.json(), indent=4))
            print("No abstract found")

def remove_jats_tags(text):
    """Remove JATS tags from text"""
    # This regular expression finds all instances of <jats:p> and </jats:p> and removes them
    cleaned_text = re.sub(r"</?jats:p>", "", text)
    return cleaned_text


def get_references(query: str, limit: int = 20) -> list[Reference]:
    """Get references from a query"""
    cr = Crossref()

    # query
    results = cr.works(query=query, limit=limit)
    # print(results["message"]["items"][0]["link"])
    refs = []
    for result in results["message"]["items"]:
        if "author" in result:
            authors = ", ".join(
                [f"{author['given']} {author['family']}" for author in result["author"]]
            )
        else:
            authors = ""

        if "published" in result:
            year = result["published"]["date-parts"][0][0]
        else:
            year = ""

        if "link" in result:
            url = result["link"][0]["URL"]

        refs.append(
            Reference(
                result["title"],
                result["DOI"],
                authors,
                year,
                url,
            )
        )

    return refs


if __name__ == "__main__":
    papers = get_references("extreme events arindam saha")
    INDEX = 3
    print(papers[INDEX])
    papers[INDEX].get_abstract()
    print(papers[INDEX].abstract)

    # for paper in papers:
    #     paper.get_citation()
    #     print(paper.citation)
