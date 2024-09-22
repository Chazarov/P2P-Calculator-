import requests
import json
import asyncio
import aiohttp
from aiohttp import ClientSession
import xml.etree.ElementTree as ET


    

async def get_curerncy_rate_BTC(char_code_currency:str, session:ClientSession = None) -> float:

    """
    :all possible options of the parameter char_code_currency see here: https://blockchain.info/ticker
    :options used in the application see in: Contexts/STATIC.py
    """

    async with session.get('https://blockchain.info/ticker') as response:
        if response.status == 200:
            json_data = await response.json()
            result = (str(json_data.get(char_code_currency).get("last"))).replace(",", ".")
            return float(result)