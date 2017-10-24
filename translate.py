from aiogoogletrans import Translator
import asyncio

def translate(text):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(_translate(text))

async def _translate(text):
    return await Translator().translate(
        text=text, src='cs', dest='en',
    )
