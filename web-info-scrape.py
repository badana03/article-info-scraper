import requests
from bs4 import BeautifulSoup

def extract_article_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract relevant information
    author = soup.find('meta', {'name': 'author'})['content'] if soup.find('meta', {'name': 'author'}) else "Author not found"
    date_published = soup.find('meta', {'name': 'date'})['content'] if soup.find('meta', {'name': 'date'}) else "Date not found"
    title = soup.find('meta', {'property': 'og:title'})['content'] if soup.find('meta', {'property': 'og:title'}) else "Title not found"
    journal_name = soup.find('meta', {'name': 'citation_journal_title'})['content'] if soup.find('meta', {'name': 'citation_journal_title'}) else "Journal name not found"
    volume = soup.find('meta', {'name': 'citation_volume'})['content'] if soup.find('meta', {'name': 'citation_volume'}) else "Volume not found"
    issue = soup.find('meta', {'name': 'citation_issue'})['content'] if soup.find('meta', {'name': 'citation_issue'}) else "Issue not found"
    pages = soup.find('meta', {'name': 'citation_firstpage'})['content'] + "-" + soup.find('meta', {'name': 'citation_lastpage'})['content'] if soup.find('meta', {'name': 'citation_firstpage'}) and soup.find('meta', {'name': 'citation_lastpage'}) else "Pages not found"
    doi = soup.find('meta', {'name': 'citation_doi'})['content'] if soup.find('meta', {'name': 'citation_doi'}) else None

    return author, date_published, title, journal_name, volume, issue, pages, doi

def format_citation(author, date_published, title, journal_name, volume, issue, pages, doi=None):
    citation = f"{author} ({date_published}). {title}. {journal_name}, {volume}({issue}), {pages}."
    if doi:
        citation += f" https://doi.org/{doi}"
    return citation

# Main program
url = input("Enter the URL of the article: ")
author, date_published, title, journal_name, volume, issue, pages, doi = extract_article_info(url)
formatted_citation = format_citation(author, date_published, title, journal_name, volume, issue, pages, doi)
print("\nFormatted Citation:")
print(formatted_citation)