import requests

from requests.adapters import HTTPAdapter, Retry

req_ses = requests.Session()

retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[ 500, 502, 503, 504 ])

req_ses.mount('https://', HTTPAdapter(max_retries=retries))