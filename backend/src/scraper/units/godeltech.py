import requests

from bs4 import BeautifulSoup

from src.scraper.celery_app import celery_app
from src.scraper.utils import extract_skills
from src.scraper.request_session import req_ses

BASE_URL = "https://www.godeltech.com/careers/all-careers/"
COMPANY = "Godel Technologies"

def scrape_job_urls():

    filtered: list[dict] = []

    response = req_ses.get(BASE_URL, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')
    cards = soup.find_all('div', {
        'class': 'job-card'
    })

    for each in cards:
        location = each.find('h4').text

        if location != 'Georgia':
            continue

        title = each.find('h3').text
        url = each.find('a')['href']

        response = req_ses.get(url, verify=False)
        soup = BeautifulSoup(response.content, 'html.parser')

        text = soup.find('section', {
            'class': 'job-card-section'
        }).text

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
