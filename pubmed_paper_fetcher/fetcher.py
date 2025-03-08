import requests
import logging

PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

class PubMedFetcher:
    def __init__(self, email: str):
        """Initialize with an email (PubMed requires this for API access)."""
        self.email = email

    def search_papers(self, query: str, max_results: int = 10):
        """Fetch paper IDs from PubMed based on the search query."""
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "json",
            "email": self.email
        }
        response = requests.get(PUBMED_SEARCH_URL, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching data: {response.status_code}")
        
        data = response.json()
        return data.get("esearchresult", {}).get("idlist", [])

    def fetch_paper_details(self, paper_ids):
        """Fetch detailed paper information using PubMed IDs."""
        if not paper_ids:
            return ""

        params = {
            "db": "pubmed",
            "id": ",".join(paper_ids),
            "retmode": "xml",  
            "email": self.email
        }

        response = requests.get(PUBMED_FETCH_URL, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching paper details: {response.status_code}")

        return response.text 
