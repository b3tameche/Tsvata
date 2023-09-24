import requests

from bs4 import BeautifulSoup

from src.scraper.celery_app import celery_app
from src.scraper.utils import extract_skills
from src.scraper.request_session import req_ses

BASE_URL = "https://sd-solutions.breezy.hr/json"
COMPANY = "SD Solutions"

def scrape_job_urls():

    filtered: list[dict] = []

    response: list[dict] = req_ses.get(BASE_URL).json()

    for each in response:
        location = each.get('location').get('name')

        if 'tbilisi' not in location.lower():
            continue

        title = each.get('name').split('|')[1].strip()
        url = each.get('url')

        response = req_ses.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')

        html = soup.find('div', {
            'class': 'description'
        })

        skill_ids = extract_skills(str(html))

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
