import asyncio
import time
import os

from aiohttp import ClientSession
from time import perf_counter as timer
from logger import LOGGER
from config import HTTP_HEADERS, get_export_filepath, get_tei_header, get_tei_closer

from .utils import get_urls


async def get_entity(session, url, total_count, current):
    async with session.get(url) as resp:
        try:
            mystr = await resp.text(encoding='utf-8')
            html = "".join([s for s in mystr.splitlines(True) if s.strip()])
            LOGGER.info(f"Fetched URL {current} of {total_count}")
        except Exception as e:
            LOGGER.error(f"failed to process {url} due to {e}")
            html = f"<item url='{url}'></item>"
        return html


async def main(apis_entity_name):
    start_time = timer()
    urls_to_fetch = get_urls(apis_entity_name)
    EXPORT_FILEPATH = get_export_filepath(apis_entity_name)
    os.remove(EXPORT_FILEPATH)

    with open(EXPORT_FILEPATH, 'w', encoding="utf-8") as f:
        f.write(get_tei_header(apis_entity_name))

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
            f.write(get_tei_closer(apis_entity_name))
    LOGGER.success(
        f"Dumped {total_count} {apis_entity_name} entities in {time.perf_counter() - start_time:0.2f} seconds into {EXPORT_FILEPATH}."
    )
    LOGGER.success(
        f"Dumped {total_count} {apis_entity_name} entities in {(time.perf_counter() - start_time)/60:0.2f} minutes into {EXPORT_FILEPATH}."
    )