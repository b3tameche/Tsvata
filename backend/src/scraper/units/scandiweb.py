import requests

from src.scraper.celery_app import celery_app
from src.scraper.utils import extract_skills
from src.scraper.request_session import req_ses

BASE_URL = "https://scandiweb.pinpointhq.com/postings.json"
COMPANY = "Scandiweb"

def extract_data_from_api():

    filtered: list[dict] = []

    params = {
        "location_id": [11786],
        "department_id": [22742, 20709, 20713, 20712]
    }

    response: dict = req_ses.get(BASE_URL, params=params).json()
    postings: list[dict] = response.get('data')

    for each in postings:
        title = each.get('title')
        url = each.get('url')

        html = each.get('key_responsibilities') + each.get('skills_knowledge_expertise')

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
    return extract_data_from_api()
