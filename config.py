"""Script configuration."""
from os import path

# Base directory of project
BASE_DIR = path.abspath(path.dirname(__file__))

# Pagination Size
BASE_LIMIT = "50"

# Base URL of the APIS instance to crawl
BASE_URL = "https://pmb.acdh.oeaw.ac.at/"

# URL Pattern for the entitiy-list endpoint
BASE_LIST_URL = "{}apis/api/entities/{}/?format=json&limit={}"

# URL Pattern for the entity TEI endpoint
TEI_URL = "{}apis/entities/tei/{}/"

# Filepath to store dumped entities
EXPORT_FILEPATH = "{}/export/list{}.xml"

# Headers to be passed to async HTTP client session.
HTTP_HEADERS = {
    "content-type": "application/xml; charset=UTF-8",
    "connection": "keep-alive",
    "accept": "*/*",
}

ENT_DICT = {
    'person': 'person',
    'place': 'place',
    'work': 'bibl',
    'institution': 'org'
}

LIMIT = True

def get_base_url(apis_entity_name):
    return BASE_LIST_URL.format(BASE_URL, apis_entity_name, BASE_LIMIT)

def get_tei_endpoint(apis_entity_name, entity_id):

    return "{}apis/entities/tei/{}/{}".format(
        BASE_URL,
        apis_entity_name,
        entity_id
    )


def get_export_filepath(apis_entity_name):
    return EXPORT_FILEPATH.format(
        BASE_DIR,
        ENT_DICT[apis_entity_name]
    )