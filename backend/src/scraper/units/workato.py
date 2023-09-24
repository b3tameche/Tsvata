import requests

from bs4 import BeautifulSoup, ResultSet

from src.scraper.celery_app import celery_app
from src.scraper.utils import extract_skills
from src.scraper.request_session import req_ses

BASE_URL = "https://boards.greenhouse.io/workato"
COMPANY = "Workato"

def scrape_job_urls():

    filtered: list[dict] = []

    response = req_ses.get(BASE_URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    cards: ResultSet = soup.find_all('div', {
        'class': "opening",
        "department_id": "4011938002",
    })
    
    for each in cards:
        location = each.find('span', 'location')

        if 'Georgia' not in location.get_text():
            continue

        title = each.find('a').text
        url = "https://boards.greenhouse.io" + each.find('a')['href']

        response = req_ses.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        text = soup.find('div', {
            'id': 'content'
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
