import requests

from logger import LOGGER
from config import get_base_url, get_tei_endpoint, LIMIT


def get_urls(apis_entity_name):
    urls = []
    next = get_base_url(apis_entity_name)
    while next:
        LOGGER.info(f"Processing URL {next}")
        response = requests.get(next)
        data = response.json()
        if LIMIT:
            next = False
        else:
            next = data['next']
        for x in data['results']:
            url = get_tei_endpoint(apis_entity_name, x['id'])
            LOGGER.info(f"adding {url}")
            urls.append(url)
    return urls
