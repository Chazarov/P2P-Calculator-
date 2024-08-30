import aiohttp
from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

class AiohttpSessionMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

    async def on_pre_process_update(self, update: types.Update, data: dict):
        session = aiohttp.ClientSession()
        data['session'] = session

    async def on_post_process_update(self, update: types.Update, result, data: dict):
        session: aiohttp.ClientSession = data.get('session')
        if session:
            await session.close()