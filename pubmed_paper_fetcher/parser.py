import re
import xml.etree.ElementTree as ET
import logging

# ✅ Define company keywords (if not already defined)
COMPANY_KEYWORDS = [
    "Pharma", "Biotech", "Inc.", "Labs", "Corporation", "Ltd", "GmbH", "S.A.", "LLC",
    "Research", "Technology", "Medical", "Healthcare", "Diagnostics", "Therapeutics",
    "Sinocelltech", "Moderna", "Pfizer", "AstraZeneca", "Novartis", "Gilead", "Regeneron",
    "Sino Biological", "Amgen", "Roche", "Merck", "Sanofi", "Bayer"
]

EMAIL_PATTERN = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

def extract_non_academic_authors(xml_response):
    """Parse XML response and extract non-academic authors + emails."""
    root = ET.fromstring(xml_response)
    papers = []

    for article in root.findall(".//PubmedArticle"):
        paper_id = article.find(".//PMID").text
        title = article.find(".//ArticleTitle").text
        pub_date = article.find(".//PubDate/Year")

        if pub_date is not None:
            pub_date = pub_date.text
        else:
            pub_date = "Unknown"

        non_academic_authors = []
        company_affiliations = []
        corresponding_author_email = None

        for author in article.findall(".//Author"):
            name = author.find("LastName")
            first_name = author.find("ForeName")
            affiliation = author.find(".//AffiliationInfo/Affiliation")

            if name is not None and first_name is not None:
                full_name = f"{first_name.text} {name.text}"
            else:
                full_name = "Unknown"

            if affiliation is not None:
                aff_text = affiliation.text.strip()
                logging.debug(f"👤 Checking author: {full_name}, Affiliation: {aff_text}")

 
                email_match = re.search(EMAIL_PATTERN, aff_text)
                if email_match:
                    corresponding_author_email = email_match.group(0)

                
                if any(keyword.lower() in aff_text.lower() for keyword in COMPANY_KEYWORDS):
                    non_academic_authors.append(full_name)
                    company_affiliations.append(aff_text)

        papers.append({
            "id": paper_id,
            "title": title,
            "pub_date": pub_date,
            "non_academic_authors": non_academic_authors,
            "company_affiliations": company_affiliations,
            "corresponding_author_email": corresponding_author_email
        })

    return papers
