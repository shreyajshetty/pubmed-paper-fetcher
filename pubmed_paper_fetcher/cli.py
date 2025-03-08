import argparse
import logging
from pubmed_paper_fetcher.fetcher import PubMedFetcher
from pubmed_paper_fetcher.parser import extract_non_academic_authors
from pubmed_paper_fetcher.csv_writer import save_to_csv


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("-f", "--file", type=str, help="Output CSV filename", default="papers.csv")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()

   
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    logging.info(f" Searching for papers with query: {args.query}")

    fetcher = PubMedFetcher(email="your-email@example.com")
    paper_ids = fetcher.search_papers(args.query)

    if not paper_ids:
        logging.warning(" No papers found!")
        return

    logging.info(f"Found {len(paper_ids)} papers. Fetching details...")

    xml_data = fetcher.fetch_paper_details(paper_ids) 

    results = []
    parsed_papers = extract_non_academic_authors(xml_data)  

    for paper in parsed_papers:
        results.append({
            "id": paper["id"],
            "title": paper["title"],
            "pub_date": paper["pub_date"],
            "non_academic_authors": paper["non_academic_authors"],
            "company_affiliations": paper["company_affiliations"]
        })

    if results:
        save_to_csv(results, args.file)
        logging.info(f" Results saved to {args.file}")
    else:
        logging.warning(" No non-academic authors found.")

if __name__ == "__main__":
    main()
