import requests
from bs4 import BeautifulSoup

def extract_article_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract metadata
    author = soup.find('meta', {'name': 'author'})
    if author:
        author = author.get('content')
    else:
        author = extract_author_from_content(soup)

    date_published = soup.find('meta', {'name': 'date'})
    if date_published:
        date_published = date_published.get('content')
    else:
        date_published = extract_date_from_content(soup)

    title = soup.find('meta', {'property': 'og:title'})
    if title:
        title = title.get('content')
    else:
        title = extract_title_from_content(soup)

    journal_name = soup.find('meta', {'name': 'citation_journal_title'})
    if journal_name:
        journal_name = journal_name.get('content')
    else:
        journal_name = extract_journal_name_from_content(soup)

    volume = soup.find('meta', {'name': 'citation_volume'})
    if volume:
        volume = volume.get('content')
    else:
        volume = extract_volume_from_content(soup)

    issue = soup.find('meta', {'name': 'citation_issue'})
    if issue:
        issue = issue.get('content')
    else:
        issue = extract_issue_from_content(soup)

    pages = None
    first_page = soup.find('meta', {'name': 'citation_firstpage'})
    last_page = soup.find('meta', {'name': 'citation_lastpage'})
    if first_page and last_page:
        pages = first_page.get('content') + "-" + last_page.get('content')
    else:
        pages = extract_pages_from_content(soup)

    doi = soup.find('meta', {'name': 'citation_doi'})
    if doi:
        doi = doi.get('content')
    else:
        doi = extract_doi_from_content(soup)

    return author, date_published, title, journal_name, volume, issue, pages, doi

def extract_author_from_content(soup):
    # Fallback method to find author from visible content
    possible_authors = soup.find_all(text=lambda text: "author" in text.lower())
    for author in possible_authors:
        if author.parent.name in ['p', 'span', 'div']:
            return author.parent.text.strip()
    return "Author not found"

def extract_date_from_content(soup):
    # Fallback method to find date from visible content
    possible_dates = soup.find_all(text=lambda text: "published" in text.lower() or "date" in text.lower())
    for date in possible_dates:
        if date.parent.name in ['p', 'span', 'div']:
            return date.parent.text.strip()
    return "Date not found"

def extract_title_from_content(soup):
    # Fallback method to find title from visible content
    if soup.title:
        return soup.title.string.strip()
    return "Title not found"

def extract_journal_name_from_content(soup):
    # Fallback method to find journal name from visible content
    possible_journal_names = soup.find_all(text=lambda text: "journal" in text.lower())
    for journal_name in possible_journal_names:
        if journal_name.parent.name in ['p', 'span', 'div']:
            return journal_name.parent.text.strip()
    return "Journal name not found"

def extract_volume_from_content(soup):
    # Fallback method to find volume from visible content
    possible_volumes = soup.find_all(text=lambda text: "volume" in text.lower())
    for volume in possible_volumes:
        if volume.parent.name in ['p', 'span', 'div']:
            return volume.parent.text.strip()
    return "Volume not found"

def extract_issue_from_content(soup):
    # Fallback method to find issue from visible content
    possible_issues = soup.find_all(text=lambda text: "issue" in text.lower())
    for issue in possible_issues:
        if issue.parent.name in ['p', 'span', 'div']:
            return issue.parent.text.strip()
    return "Issue not found"

def extract_pages_from_content(soup):
    # Fallback method to find pages from visible content
    possible_pages = soup.find_all(text=lambda text: "pages" in text.lower())
    for pages in possible_pages:
        if pages.parent.name in ['p', 'span', 'div']:
            return pages.parent.text.strip()
    return "Pages not found"

def extract_doi_from_content(soup):
    # Fallback method to find DOI from visible content
    possible_dois = soup.find_all(text=lambda text: "doi" in text.lower())
    for doi in possible_dois:
        if doi.parent.name in ['p', 'span', 'div']:
            return doi.parent.text.strip()
    return None

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
