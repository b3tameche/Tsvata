import requests

from bs4 import BeautifulSoup, ResultSet
from urllib.parse import urlparse

from src.scraper.celery_app import celery_app
from src.scraper.utils import extract_skills
from src.scraper.request_session import req_ses

BASE_URL = "https://omedia.dev/careers"
HOST = "https://" + urlparse(BASE_URL).hostname
COMPANY = "Omedia"

def scrape_job_urls():

    filtered: list[dict] = []

    response = req_ses.get(BASE_URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    cards: ResultSet = soup.find_all('div', {
        'class': "views-row"
    })

    for each in cards:
        card = each.find('a', {'class': 'ei-title'})

        title = card.text.strip()
        url = HOST + card.get('href')

        response = req_ses.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        content = soup.find('div', {
            'class': 'ei-body'
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

    filtered.pop() # "didn't find a suitable position?"

    return filtered

@celery_app.task(name=__file__)
def main(arg=None):
    return scrape_job_urls()
