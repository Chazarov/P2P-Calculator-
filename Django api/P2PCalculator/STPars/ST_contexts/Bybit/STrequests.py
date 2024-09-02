import asyncio
import aiohttp
import json

from .Static import TOKENS, CURRENCIES, BASE_URL, PREFERENCES, PAYMENTS, TRADE_ROLE, SM_NAME
from ..BASE_STATIC import USER_NAME, PRICE, MIN_AMOUNT, USER_ID, ADV_ID





def make_payload(token: str, currency: str, payment: str, trade_role:str, page: int) -> dict:
    payload = {
        "tokenId": token,
        "currencyId": currency,
        "payment": [payment],
        "side": trade_role,
        "size": str(PREFERENCES.NUMBER_OF_UNITS_PER_PAGE),
        "page": str(page),
        "amount": "",
        "authMaker": "false",
        "canTrade": "false",
    }
    return payload

async def fetch_data(session, url, payload):
    async with session.post(url, json=payload) as response:
        if response.status != 200:
            print(f"Bybit Error: status-code {response.status}\n reason: {response.reason}\n content: {response.content}\n")
            return None

        response_json = await response.json()

        if response_json.get("ret_code") != 0:
            ret_msg = response_json.get("ret_msg", "Unknown error")
            print(f"Ошибка: {ret_msg}")
            return None

    return response_json.get("result").get("items")

async def get_data(session:aiohttp.ClientSession) -> dict:


    result_data = {}

    CURRENCIES_LIST = CURRENCIES.to_list()
    TOKENS_LIST = TOKENS.to_list()
    PAYMENTS_LIST = PAYMENTS.to_list()
    TRADE_ROLES = TRADE_ROLE.to_list()



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

                    

                    pages_count = 1

                    while pages_count <= PREFERENCES.NUMBER_OF_PAGES_TO_PARSE:
                        payload = make_payload(TOKEN, CURRENCY, PAYMENT, ROLE, pages_count)
                        page_data = await fetch_data(session, BASE_URL, payload)

                        if not page_data:
                            continue
                        
                        # print(f"Bybit---{ROLEN[ROLE]}---{CN[CURRENCY]}---{TN[TOKEN]}---{PN[PAYMENT]}---{pages_count}\n")
                        page_data = formed_data(page_data)
                        
                        pages_count += 1
                        result_data[ROLEN[ROLE]][CN[CURRENCY]][TN[TOKEN]][PN[PAYMENT]] += page_data

    return result_data


def formed_data(data:dict) -> dict:
    result_data = []
    for i in range(len(data)):
        result_data.append({})
        try:
            result_data[i][USER_NAME] = data[i].get("nickName")
            result_data[i][PRICE] = data[i].get("price")
            result_data[i][MIN_AMOUNT] = data[i].get("minAmount")
            result_data[i][USER_ID] = data[i].get("userId")
            result_data[i][ADV_ID] = data[i].get("id")
        except Exception as e:
            print(">>>Unpack request data Exception:  " + str(e) + "\n\n")
    return result_data





    