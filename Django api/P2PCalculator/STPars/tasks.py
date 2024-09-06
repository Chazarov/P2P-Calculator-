import asyncio
import aiohttp
import aiofiles
import json
from pathlib import Path

from django.conf import settings

from P2PCalculator.PREFERENCES import SM_DATA_FILE_NAME, UPDATE_RATE


from .ST_contexts.Bybit.STrequests import get_data as b_get_data
from .ST_contexts.Bybit.Static import SM_NAME as B_SM_NAME
from .ST_contexts.HTX.STrequests import get_data as h_get_data
from .ST_contexts.HTX.Static import SM_NAME as H_SM_NAME
from .ST_contexts.Bitget.STrequests import get_data as bi_get_data
from .ST_contexts.Bitget.Static import SM_NAME as BI_SM_NAME




finish_thread = [False]



FILE_PATH = Path(settings.MEDIA_ROOT).joinpath(SM_DATA_FILE_NAME)


refresh_Bybit_done = [True]
refresh_HTX_done = [True]
refresh_Bitget_done = [True]

refresh_lock = asyncio.Lock()





async def get_current_data():
    async with aiofiles.open(FILE_PATH, "r", encoding='utf-8') as file:
        content = await file.read()
        return json.loads(content)
    
async def write_current_data(data):

    async with aiofiles.open(FILE_PATH, 'w', encoding='utf-8') as file:
        await file.write(json.dumps(data, ensure_ascii=False, indent=4))



async def refresh(refresh_function, SM_NAME:str, flag:list, session:aiohttp.ClientSession):
    if(flag[0] == True):
        flag[0] = False
    else: return

    data = await get_current_data()

    Fresh_data = await refresh_function(session = session)
    data[SM_NAME] = Fresh_data
    await write_current_data(data)
    await asyncio.sleep(UPDATE_RATE)
    flag[0] = True





async def refresh_data():
    async with aiohttp.ClientSession() as session:
        await refresh(bi_get_data, BI_SM_NAME, refresh_Bitget_done, session)
        print(">> Bitget update completed <<")
        await refresh(b_get_data, B_SM_NAME, refresh_Bybit_done, session)
        print(">> Bybit update completed <<")
        await refresh(h_get_data, H_SM_NAME, refresh_HTX_done, session)
        print(">> HTX update completed <<")
            



