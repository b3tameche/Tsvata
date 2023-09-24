import requests

from src.scraper.celery_app import celery_app
from src.scraper.utils import extract_skills
from src.scraper.request_session import req_ses

BASE_URL = "https://api.crocosquad.ge/api/V1/job/list"
CONSTRUCT_URL = "https://crocosquad.com/jobs/"
COMPANY = "Crocosquad"

def extract_data_from_api():
    filtered: list[str] = []

    response = req_ses.get(BASE_URL, verify=False)
    jsoned: dict = response.json()

    data: list[dict] = jsoned.get('data')

    for each in data:

        title = each.get('title')
        url = CONSTRUCT_URL + str(each.get('id')) + "/" + each.get('slug')

        html = each.get('knowledge_description') + each.get('have_to_do_description')

        skills = extract_skills(html)

        if (len(skills) == 0):
            continue

        filtered.append({
            'title': title,
            'url': url,
            'company': COMPANY,
            'skills': skills
        })
    
    return filtered

@celery_app.task(name=__file__)
def main(arg=None):
    return extract_data_from_api()
