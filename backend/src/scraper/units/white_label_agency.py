import requests

from urllib.parse import urlparse

from src.scraper.celery_app import celery_app
from src.scraper.utils import extract_skills
from src.scraper.request_session import req_ses

BASE_URL = "https://whitelabelagency.bamboohr.com/careers/list"
CONSTRUCT_URL = "https://" + urlparse(BASE_URL).netloc + "/careers/"
COMPANY = "White Label Agency"

def scrape_job_urls():

    filtered: list[dict] = []

    response = req_ses.get(BASE_URL)

    jsoned: dict = response.json()

    results: list[dict] = jsoned.get('result')

    for each in results:
        location = each.get('location').get('state')
        department = each.get('departmentLabel')

        if location is None or 'tbilisi' not in location.lower():
            continue

        if department is None or department.lower().strip() not in ('development', 'design'):
            continue

        title = each.get('jobOpeningName')
        url = CONSTRUCT_URL + each.get('id') + "/detail"

        response = req_ses.get(url)

        jsoned = response.json().get('result')
        html = jsoned.get('jobOpening').get('description')

        skill_ids = extract_skills(html)

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
