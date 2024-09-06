import asyncio
import aiohttp
import aiofiles
import json
from pathlib import Path
from django.core.cache import cache

from celery import shared_task

from django.conf import settings

from P2PCalculator.PREFERENCES import SM_DATA_FILE_NAME, UPDATE_RATE, LOCK_EXPIRE


from .ST_contexts.Bybit.STrequests import get_data as b_get_data
from .ST_contexts.Bybit.Static import SM_NAME as B_SM_NAME
from .ST_contexts.HTX.STrequests import get_data as h_get_data
from .ST_contexts.HTX.Static import SM_NAME as H_SM_NAME
from .ST_contexts.Bitget.STrequests import get_data as bi_get_data
from .ST_contexts.Bitget.Static import SM_NAME as BI_SM_NAME





FILE_PATH = Path(settings.MEDIA_ROOT).joinpath(SM_DATA_FILE_NAME)

refresh_lock = asyncio.Lock()




def acquire_lock(lock_id):
    return cache.add(lock_id, "locked", LOCK_EXPIRE)



def release_lock(lock_id):
    cache.delete(lock_id)



async def get_current_data():
    async with aiofiles.open(FILE_PATH, "r", encoding='utf-8') as file:
        content = await file.read()
        return json.loads(content)
    


async def write_current_data(data):
    async with aiofiles.open(FILE_PATH, 'w', encoding='utf-8') as file:
        await file.write(json.dumps(data, ensure_ascii=False, indent=4))



async def refresh(refresh_function, SM_NAME:str, session:aiohttp.ClientSession):

    data = await get_current_data()

    Fresh_data = await refresh_function(session = session)
    data[SM_NAME] = Fresh_data
    await write_current_data(data)



@shared_task
async def refresh_data_BITGET():
    async with aiohttp.ClientSession() as session:
        await refresh(bi_get_data, BI_SM_NAME, session)
        print(">> Bitget update completed <<")
        return "Success"



@shared_task
async def refresh_data_BYBIT():
    async with aiohttp.ClientSession() as session:
        await refresh(b_get_data, B_SM_NAME, session)
        print(">> Bybit update completed <<")
        return "Success"



@shared_task
async def refresh_data_HTX():
    async with aiohttp.ClientSession() as session:
        await refresh(h_get_data, H_SM_NAME, session)
        print(">> HTX update completed <<")
        return "Success"

            



