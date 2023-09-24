import requests

from functools import reduce

from src.scraper.celery_app import celery_app
from src.scraper.utils import extract_skills
from src.scraper.request_session import req_ses

BASE_URL = "https://admin.flatrocktech.com/wp-admin/admin-ajax.php?action=frt_jobs"
CONSTRUCT_URL = "https://flatrocktech.com/careers/"
COMPANY = "FlatRockTech"

def extract_data_from_api():
    filtered: list[dict] = []

    response: list[dict] = req_ses.get(BASE_URL).json()

    for each in response:
        locations = list(map(lambda x: x.lower().strip(), each.get('locations')))

        if 'tbilisi' not in locations:
            continue

        department = each.get('occupation_category')
        department_keywords = ['software', 'data', 'quality', 'web']

        department_check_passed = reduce(lambda x, y: x or (y in department.lower()), department_keywords, False) if department is not None else False

        if not department_check_passed:
            continue

        title = each.get('name')
        url = CONSTRUCT_URL + each.get('slug')

        responsibilities = each.get('main_responsibilities')
        requirements = each.get('requirements')

        html = responsibilities + requirements

        skill_ids = extract_skills(html)

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
    return extract_data_from_api()
