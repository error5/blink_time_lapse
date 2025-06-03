import asyncio
import json
import ssl
from datetime import datetime

from aiohttp import ClientSession, TCPConnector
from blinkpy.auth import Auth
from blinkpy.blinkpy import Blink
from blinkpy.helpers.util import json_load

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

    auth = Auth(await json_load(CREDFILE), session=session)
    blink.auth = auth
    await blink.start()
    return blink, session


async def main():
    """Run the blink app and grab a photo."""
    blink, session = await start()

    camera = blink.cameras["Front Garden"]
    await camera.snap_picture()  # Take a new picture with the camera
    await blink.refresh()  # Get new information from server

    with open(
        "front_garden.log", "a"
    ) as file:  # log camera details trend temp and voltage in future.
        file.write(json.dumps(camera.attributes) + "\n")

    now = datetime.now()
    formatted = now.strftime("%Y-%m-%d-%H%M")

    await camera.image_to_file(f"front_garden_{formatted}.jpg")
    await session.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


# Suggested Photo Frequency Options (During Daylight Only):

# Every 6 hours (2xday) : 8 AM and 2 PM
# Good for slow changes

# Every 4 hours (3xday) : 8 AM, 12 PM, 4 PM
# More natural flow, captures morning/midday/evening light

# Every 2 hours (7x/day) : 6 AM, 8 AM, 10 AM, 12 PM, 2 PM, 4 PM, 6 PM
# Very smooth, excellent for fast plant movements like flowers opening
