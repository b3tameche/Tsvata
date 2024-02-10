import requests

from bs4 import BeautifulSoup

from src.scraper.celery_app import celery_app
from src.scraper.utils import extract_skills
from src.scraper.request_session import req_ses

BASE_URL = "https://careers.exadel.com/jm-ajax/get_listings/"
COMPANY = "Exadel"

def scrape_job_urls():

    filtered: list[dict] = []

    params = {
        "filter_job_type": "georgia",
        "filter_post_status": "publish",
        "per_page": "100",
        "orderby": "featured",
        "order": "DESC",
        "page": 1,
        "show_pagination": "false",
    }

    response = req_ses.get(BASE_URL, params=params)
    html = response.json()['html']

    soup = BeautifulSoup(html, 'html.parser')

    cards = soup.find_all('li', {
        'class': "careers-results-item"
    })

    for each in cards:
        title = each.find('div', 'careers-results-item__job-title').text
        url = list(map(lambda x: x['href'], filter(lambda x: x.text.strip() == "View", each.find_all('a'))))[0]

        response = req_ses.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        text = soup.find('div', {
            'class': 'job_description'
        }).text

        skill_ids = extract_skills(text)

        if (len(skill_ids) == 0):
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
