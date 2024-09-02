import time
import json
import os
import hashlib
import hmac
import base64
import urllib.parse


import aiohttp
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())


from .Static import TOKENS, CURRENCIES, BASE_URL, RELATIVE_URL, PREFERENCES, PAYMENTS, TRADE_ROLE, SM_NAME
from ..BASE_STATIC import USER_NAME, PRICE, MIN_AMOUNT, USER_ID, ADV_ID





def generate_access_sign(secret_key, timestamp, method, request_path, query_string, body):

    method = method.upper()
    message = f'{timestamp}{method}{request_path}?{query_string}{body}'
    signature = hmac.new(secret_key.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).digest()
    access_sign = base64.b64encode(signature).decode('utf-8')

    return access_sign



def make_headers(query_string:str):

    api_key = os.getenv("API_KEY_BITGET")
    secret_key = os.getenv("SEKRET_KEY_BITGET")
    passphrase = os.getenv("CODE_PHRASE_BITGET")

    timestamp = str(int(time.time() * 1000))
    signature = generate_access_sign(secret_key = secret_key, timestamp = timestamp, method = "GET", request_path = RELATIVE_URL, query_string = query_string, body = "")
    
    headers = {
        "ACCESS-KEY" : str(api_key),
        "ACCESS-SIGN" : str(signature),
        "ACCESS-PASSPHRASE" : str(passphrase),
        "ACCESS-TIMESTAMP" : str(timestamp),
        "locale" : "en-US",
        "Content-Type" : "application/json",
    }
    return headers



def make_params(token: str, currency: str, payment: str, trade_role:str) -> dict:

    current_time = int(time.time() * 1000)
    start_time = current_time - 7 * 24 * 60 * 1000


    params = {
        "startTime" : str(start_time),
        "side" : str(trade_role),
        "coin" : str(token),
        "language" : "en-US",
        "fiat" : str(currency),
        "payMethodId" : str(payment),
        "sourceType" : "competitior",
        "pageSize" : str(PREFERENCES.NUMBER_OF_UNITS_PER_PAGE),    
    }

    return params



async def fetch_data(session:aiohttp.ClientSession, url, params, headers):

    
    async with session.get(url, params = params, headers = headers) as response:
        
        if response.status != 200:
            print(f"Bitget Error: status-code {response.status}\n reason: {response.reason}\n content: {response.content}\n")

            try:
                response_json = await response.json()
                print(str(response_json) + "\n\n")
            except Exception as e:
                print("Fall to get data in responce: " + str(e) + "\n\n\n")

            return None

        response_json = await response.json()

        if response_json.get("code") != "00000":
            ret_msg = response_json.get("msg", "Unknown error")
            print(f"Ошибка: {ret_msg}")
            return None

    return response_json.get("data").get("advList")




async def get_data(session:aiohttp.ClientSession) -> dict:

    result_data = {}

    CURRENCIES_LIST = CURRENCIES.to_list()
    TOKENS_LIST = TOKENS.to_list()
    PAYMENTS_LIST = PAYMENTS.to_list()
    TRADE_ROLES = TRADE_ROLE.to_list()


    print(PAYMENTS_LIST)

    # Dictionaries with parameter names for easy perception
    CN = CURRENCIES.to_dict()
    TN = TOKENS.to_dict()
    PN = PAYMENTS.to_dict()
    ROLEN = TRADE_ROLE.to_dict()

   


    for ROLE in TRADE_ROLES:
        result_data[ROLEN[ROLE]] = {}
        for CURRENCY in CURRENCIES_LIST:
            result_data[ROLEN[ROLE]][CN[CURRENCY]] = {}
            for TOKEN in TOKENS_LIST:
                result_data[ROLEN[ROLE]][CN[CURRENCY]][TN[TOKEN]] = {}
                for PAYMENT in PAYMENTS_LIST:
                    result_data[ROLEN[ROLE]][CN[CURRENCY]][TN[TOKEN]][PN[PAYMENT]] = []

                    
                    params = make_params(TOKEN, CURRENCY, PAYMENT, ROLE)
                    query_string = urllib.parse.urlencode(params)

                    # print(f"Bitget---{ROLEN[ROLE]}---{CN[CURRENCY]}---{TN[TOKEN]}---{PN[PAYMENT]}---\n")
                    page_data = await fetch_data(session, BASE_URL, params, headers = make_headers(query_string = query_string))

                    

                    if not page_data:
                        continue
                    
                    
                    page_data = formed_data(page_data)
                    
                    result_data[ROLEN[ROLE]][CN[CURRENCY]][TN[TOKEN]][PN[PAYMENT]] += page_data

    return result_data



def formed_data(data:dict) -> dict:
    result_data = []
    for i in range(len(data)):
        result_data.append({})
        try:
            result_data[i][USER_NAME] = data[i].get("merchantCertifiedResult")
            result_data[i][PRICE] = data[i].get("price")
            result_data[i][MIN_AMOUNT] = data[i].get("minTradeAmount")
            result_data[i][USER_ID] = data[i].get("userId")
            result_data[i][ADV_ID] = data[i].get("advId")

        except Exception as e:
            print(">>>Unpack request data Exception:  " + str(e) + "\n\n")
    return result_data





    