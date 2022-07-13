import asyncio
from aiohttp import ClientSession
from time import perf_counter as timer


import time
from logger import LOGGER
from config import HTTP_HEADERS, get_export_filepath

from .utils import get_urls


async def get_entity(session, url, total_count, current):
    async with session.get(url) as resp:
        mystr = await resp.text(encoding='utf-8')
        html = "".join([s for s in mystr.splitlines(True) if s.strip()])
        LOGGER.info(f"Fetched URL {current} of {total_count}")
        return html


async def main(apis_entity_name):
    start_time = timer()
    urls_to_fetch = get_urls(apis_entity_name)
    EXPORT_FILEPATH = get_export_filepath(apis_entity_name)

    with open(EXPORT_FILEPATH, 'w', encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<TEI xmlns="http://www.tei-c.org/ns/1.0">\n')

        async with ClientSession(headers=HTTP_HEADERS) as session:
            total_count = len(urls_to_fetch)
            tasks = []
            for current, url in enumerate(urls_to_fetch):
                tasks.append(
                    asyncio.ensure_future(
                        get_entity(session, url, total_count, current)
                    )
                )

            all_entities = await asyncio.gather(*tasks)
            for ent in all_entities:
                f.write(f"{ent}\n")
            f.write('</TEI>')
    LOGGER.success(
        f"Executed {__name__} in {time.perf_counter() - start_time:0.2f} seconds."
    )
    LOGGER.success(
        f"Executed {__name__} in {(time.perf_counter() - start_time)/60:0.2f} minutes."
    )