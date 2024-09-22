import requests
import json
import asyncio
import aiohttp
from aiohttp import ClientSession
import xml.etree.ElementTree as ET



    
async def get_currency_rate_RUB(char_code_currency:str, session:ClientSession = None):

    """
    :all possible options of the parameter char_code_currency see here: https://www.cbr.ru/scripts/XML_daily.asp
    :options used in the application see in: Contexts/STATIC.py
    """
   
    async with session.get('https://www.cbr.ru/scripts/XML_daily.asp') as response:
        text_responce = await response.text()
        get_value = ET.fromstring(text_responce).find(f"./Valute[CharCode='{char_code_currency}']/Value")
        result = get_value.text.replace(',', '.')
        return float(result)