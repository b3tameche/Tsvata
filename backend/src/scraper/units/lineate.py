import requests

from bs4 import BeautifulSoup
from urllib.parse import urlparse

from src.scraper.celery_app import celery_app
from src.scraper.utils import extract_skills
from src.scraper.request_session import req_ses

BASE_URL = "https://boards.greenhouse.io/lineate"
HOST = "https://" + urlparse(BASE_URL).hostname
COMPANY = "Lineate"

def scrape_job_urls():

    filtered: list[dict] = []

    response = req_ses.get(BASE_URL)

    soup = BeautifulSoup(response.text, "html.parser")

    locators = soup.find_all('h3')

    for each in locators:
        department = each.text
        if (department == 'Production'):
            section = each.find_parent('section')

    divs = section.find_all('div')

    for div in divs:
        url = HOST + div.find('a')['href']
        title = div.find('a').text

        response = req_ses.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        content = soup.find('div', {
            'id': 'content'
        })

        text = content.text

        skill_ids = extract_skills(text)

        if len(skill_ids) == 0:
            continue

        filtered.append({
            'title': title,
            'url': url,
            'company': COMPANY,
            'skills': skill_ids
        })
    
    return filtered

@celery_app.task(name=__file__)
def main(arg=None):
    return scrape_job_urls()
