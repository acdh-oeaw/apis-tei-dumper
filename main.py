"""Script entry point."""
import asyncio
import time

from config import ENT_DICT
from apis_tei_dumper import main
from time import perf_counter as timer
from logger import LOGGER

if __name__ == "__main__":
    start_time = timer()
    for key, _ in ENT_DICT.items():
        try:
            asyncio.run(main(key))
        except Exception as e:
            LOGGER.error(
                f"Looks like something went wrong dumpit {key} due to {e}"
            )
        time.sleep(5)
    LOGGER.success(
        f"FINISHED in {time.perf_counter() - start_time:0.2f} seconds."
    )
    LOGGER.success(
        f"FINISHED in {(time.perf_counter() - start_time)/60:0.2f} minutes."
    )
