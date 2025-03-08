import csv

def save_to_csv(data, filename="papers.csv"):
    """Save extracted data to a CSV file with proper headers."""
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

       
        writer.writerow(["PubmedID", "Title", "Publication Date", "Non-academic Authors", "Company Affiliations", "Corresponding Author Email"])

        for paper in data:
            writer.writerow([
                paper.get("id", "N/A"),
                paper.get("title", "N/A"),
                paper.get("pub_date", "N/A"),
                ", ".join(paper.get("non_academic_authors", [])),  
                ", ".join(paper.get("company_affiliations", [])),  
                paper.get("corresponding_author_email", "N/A")  
            ])

    print(f" Results saved to {filename}")
