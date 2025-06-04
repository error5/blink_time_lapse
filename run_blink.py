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

    iso_time = datetime.now().replace(microsecond=0).isoformat().replace(":", "-")

    with open(
        "front_garden.log", "a"
    ) as file:  # log camera details trend temp and voltage in future.
        log_entry = camera.attributes.copy()
        log_entry["iso_time"] = iso_time

        file.write(json.dumps(log_entry) + "\n")

    await camera.image_to_file(f"front_garden_{iso_time}.jpg")
    await session.close()


if __name__ == "__main__":
    asyncio.run(main())
