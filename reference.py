"""Module to extract reference from a query"""

from dataclasses import dataclass
from habanero import Crossref, cn


@dataclass
class Reference:
    """Class to store information about a reference"""

    title: str
    doi: str
    authors: str = ""
    year: str = ""
    citation: str = ""

    def __repr__(self):
        return f"{self.title} ({self.doi})"

    def get_citation(self, typ: str = "bibentry"):
        """Get citation from a reference"""
        string = cn.content_negotiation(ids=self.doi, format=typ)
        string = string.replace(", ", "\n")
        self.citation = string


def get_references(query: str, limit: int = 20) -> list[Reference]:
    """Get references from a query"""
    cr = Crossref()

    # query
    results = cr.works(query=query, limit=limit)
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

        refs.append(
            Reference(
                result["title"],
                result["DOI"],
                authors,
                year,
            )
        )

    return refs


if __name__ == "__main__":
    papers = get_references("extreme events arindam saha")
    print(papers)

    # for paper in papers:
    #     paper.get_citation()
    #     print(paper.citation)
