"""Script entry point."""
import asyncio

from config import ENT_DICT
from apis_tei_dumper import main

if __name__ == "__main__":
    for key, _ in ENT_DICT.items():
        asyncio.run(main(key))
