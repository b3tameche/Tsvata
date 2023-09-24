import requests

from functools import reduce
from urllib.parse import urlparse

from src.scraper.celery_app import celery_app
from src.scraper.utils import extract_skills
from src.scraper.request_session import req_ses

BASE_URL = "https://spaceinternational.bamboohr.com/careers/list"
CONSTRUCT_URL = "https://" + urlparse(BASE_URL).netloc + "/careers/"
COMPANY = "Space"

def scrape_job_urls():

    filtered: list[dict] = []

    response = req_ses.get(BASE_URL)
    results: list[dict] = response.json().get('result')

    for each in results:
        department: str = each.get('departmentLabel')
        department_keywords = ['backend', 'software', 'devops', 'engineering']
        
        flag = reduce(lambda x, y: x or (y in department.lower()), department_keywords, False) if department is not None else True

        if not flag:
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
