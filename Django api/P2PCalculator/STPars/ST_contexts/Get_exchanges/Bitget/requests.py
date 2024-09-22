import requests
import json
import asyncio
import aiohttp
from aiohttp import ClientSession
import xml.etree.ElementTree as ET



    
async def get_single_ticker(pair:str, session:ClientSession = None) -> float:

    """
    :all possible options of the parameter pair see here: https://api.bitget.com/api/spot/v1/public/products
    :options used in the application see in: Contexts/STATIC.py
    """
    
    params = {
        "symbol": pair
    }
    
    async with session.get('https://api.bitget.com/api/spot/v1/market/ticker', params = params) as response:
        if response.status == 200:

            data_json = await response.json()
            result = data_json.get("data").get("close")
            result = result.replace(",", ".")
                
            return float(result)