import asyncio
import aiohttp
import aiofiles
import redis
import os
import json
import json
import logging
from pathlib import Path
from django.core.cache import cache

from celery import shared_task
from celery_singleton import Singleton

from django.conf import settings

from P2PCalculator import PREFERENCES


from .ST_contexts.Bybit.STrequests import get_data as b_get_data
from .ST_contexts.Bybit.Static import SM_NAME as B_SM_NAME
from .ST_contexts.HTX.STrequests import get_data as h_get_data
from .ST_contexts.HTX.Static import SM_NAME as H_SM_NAME
from .ST_contexts.Bitget.STrequests import get_data as bi_get_data
from .ST_contexts.Bitget.Static import SM_NAME as BI_SM_NAME






# FILE_PATH = Path(settings.MEDIA_ROOT).joinpath(SM_DATA_FILE_NAME)
refresh_lock = asyncio.Lock()





empty_SM_data = {

}





@shared_task(base = Singleton)
def sync_refresh_data_BITGET(task_id=None):
    asyncio.run(refresh_data_BITGET())
    return ">> Bitget update completed <<"



@shared_task(base = Singleton)
def sync_refresh_data_BYBIT(task_id=None):
    asyncio.run(refresh_data_BYBIT())
    return ">> Bybit update completed <<"



@shared_task(base = Singleton)
def sync_refresh_data_HTX(task_id=None):
    asyncio.run(refresh_data_HTX())
    return ">> HTX update completed <<"



# async def get_current_data():
#     async with aiofiles.open(FILE_PATH, "r", encoding='utf-8') as file:
#         content = await file.read()
#         return json.loads(content)

def get_current_data():
    print(os.getenv("REDIS_PASS"))
    r = redis.Redis(host=PREFERENCES.REDIS_HOST, port=6379, password = os.getenv("REDIS_PASS"), decode_responses=True)
    stored_data_string = r.get(PREFERENCES.REDIS_SM_DATA_KEY)
    if(stored_data_string):
        stored_json_data = json.loads(stored_data_string)
        r.close()
        return stored_json_data
    else:
        return {}

# async def write_current_data(data):
#     async with aiofiles.open(FILE_PATH, 'w', encoding='utf-8') as file:
#         await file.write(json.dumps(data, ensure_ascii=False, indent=4))

async def write_current_data(data):
    r = redis.Redis(host=PREFERENCES.REDIS_HOST, port=6379, db=0, password = os.getenv("REDIS_PASS"), decode_responses=True)
    json_string = json.dumps(data)
    redis.set(PREFERENCES.SM_DATA_FILE_NAME, json_string)
    redis.close()


async def refresh(refresh_function, SM_NAME:str, session:aiohttp.ClientSession):

    data = get_current_data()

    Fresh_data = await refresh_function(session = session)
    data[SM_NAME] = Fresh_data
    write_current_data(data)



async def refresh_data_BITGET():
    async with aiohttp.ClientSession() as session:
        await refresh(bi_get_data, BI_SM_NAME, session)



async def refresh_data_BYBIT():
    async with aiohttp.ClientSession() as session:
        await refresh(b_get_data, B_SM_NAME, session)



async def refresh_data_HTX():
    async with aiohttp.ClientSession() as session:
        await refresh(h_get_data, H_SM_NAME, session)

            



