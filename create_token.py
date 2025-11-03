import asyncio
import ssl

from aiohttp import ClientSession
from blinkpy.blinkpy import Blink
from blinkpy.auth import Auth, BlinkTwoFARequiredError

CREDFILE = ".credentials"

async def start():
    """create token and save to credentials file"""

    blink = Blink(session=ClientSession())
    try:
        await blink.start()
    except BlinkTwoFARequiredError:
        await blink.prompt_2fa()

    await blink.save(CREDFILE)

    return blink

if __name__ == "__main__":
    asyncio.run(start())

