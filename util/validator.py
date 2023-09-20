import asyncio
from aiohttp import ClientSession
import pymyq
from util.config import settings


async def get_garage_state() -> None:
    """Create the aiohttp session and run."""
    async with ClientSession() as websession:
        myq = await pymyq.login('michaelkwasi@gmail.com ', 'Vermontishome1', websession)
        devices = myq.covers
        return devices[settings["garage"]["id"]].state


# TODO: May be moving away from myq api soon
def garage_is_open():
    garage_state = asyncio.get_event_loop().run_until_complete(get_garage_state())
    return False if garage_state == 'closed' else True

