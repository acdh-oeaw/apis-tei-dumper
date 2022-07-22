"""Script configuration."""
import os
from datetime import datetime


# Base directory of project
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
EXPORT_DIR = os.path.join(BASE_DIR, 'export')

# Pagination Size
BASE_LIMIT = "50"

# Base URL of the APIS instance to crawl
BASE_URL = "https://pmb.acdh.oeaw.ac.at/"

# URL Pattern for the entitiy-list endpoint
BASE_LIST_URL = "{}apis/api/entities/{}/?format=json&limit={}"

# URL Pattern for the entity TEI endpoint
TEI_URL = "{}apis/entities/tei/{}/"

# Filepath to store dumped entities
EXPORT_FILEPATH = "{}/list{}.xml"

# Headers to be passed to async HTTP client session.
HTTP_HEADERS = {
    "content-type": "application/xml; charset=UTF-8",
    "connection": "keep-alive",
    "accept": "*/*",
}

ENT_DICT = {
    'person': 'person',
    'place': 'place',
    # 'work': 'bibl',
    'institution': 'org'
}
if os.environ.get('LIMIT'):
    LIMIT = True
else:
    LIMIT = False

TEI_HEADER = """<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
    <teiHeader>
        <fileDesc>
           <titleStmt>
              <title>list{}.xml</title>
           </titleStmt>
           <publicationStmt>
              <p>Publication Information</p>
           </publicationStmt>
           <sourceDesc>
              <p>Information about the source</p>
           </sourceDesc>
        </fileDesc>
       <revisionDesc>
          <change when-iso="{}">serialized</change>
       </revisionDesc>
    </teiHeader>
    <text>
        <body>
           <p>Some text here.</p>
           <list{}>
"""

TEI_CLOSER = """
         </list{}>
      </body>
  </text>
</TEI>
"""

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
        EXPORT_DIR,
        ENT_DICT[apis_entity_name]
    )


def get_tei_header(apis_entity_name):
    header = TEI_HEADER.format(
        ENT_DICT[apis_entity_name],
        datetime.today().strftime('%Y-%m-%d'),
        ENT_DICT[apis_entity_name].capitalize()
    )
    return header


def get_tei_closer(apis_entity_name):
    closer = TEI_CLOSER.format(
        ENT_DICT[apis_entity_name].capitalize()
    )
    return closer
