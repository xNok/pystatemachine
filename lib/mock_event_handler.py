from random import randint
from time import sleep

import asyncio

async def mock_random_time_handler(name="", expected_state="ok", time=1):

    await asyncio.sleep(time)

    event = {"name": name, "state": expected_state, 'duration': time}

    return event