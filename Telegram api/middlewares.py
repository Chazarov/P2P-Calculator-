from typing import Any, Awaitable, Callable, Dict

import aiohttp
from aiogram import types
from aiogram import BaseMiddleware





class AiohttpSessionMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: types.TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        async with aiohttp.ClientSession() as session:
            data['session'] = session
            return await handler(event, data)