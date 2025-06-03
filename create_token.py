import asyncio
import ssl

from aiohttp import ClientSession, TCPConnector
from blinkpy.blinkpy import Blink

CREDFILE = ".credentials"


async def start():
    # Create an SSL context that disables certificate verification
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    # Apply the context to the aiohttp connector
    connector = TCPConnector(ssl=ssl_context)
    session = ClientSession(connector=connector)

    blink = Blink(session=session)
    await blink.start()
    return blink, session


async def main():
    """create token and save to credentials file"""
    blink, session = await start()

    await blink.save(CREDFILE)

    await session.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
