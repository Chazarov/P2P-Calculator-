import asyncio
import json
import aiohttp

from .Static import TOKENS, CURRENCIES, BASE_URL, PREFERENCES, PAYMENTS, TRADE_ROLE
from ..BASE_STATIC import USER_NAME, PRICE, MIN_AMOUNT, USER_ID, ADV_ID





def make_params(token: str, currency: str, payment: str, trade_role:str, page: int):


    params = {
        "coinId": str(token),
        "currency": str(currency),
        "tradeType": str(trade_role),
        "currPage": str(page),
        "payMethod": str(payment),
        "acceptOrder": "-1",
        "country": "",
        "blockType": "general",
        "online": "1",
        "range": "0",
        "amount": "",
        "isThumbsUp": "false",
        "isMerchant": "false",
        "isTraded": "false",
        "onlyTradable": "false",
        "isFollowed": "false",
        "makerCompleteRate": 0
    }

    return params

async def fetch_page(session, url, params):

    async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=PREFERENCES.TIMEOUT)) as response:
        if response.status != 200:
            print(f"HTX Error: status-code {response.status}\n reason: {response.reason}\n content: {response.content}\n")
            return None

        response_json = await response.json()
        if response.status != 200 or response_json.get("code") != 200:
            print(f"HTX Error: status-code {response.status}\n reason: {response.reason}\n content: {response.content}\n")
            ret_msg = response_json.get("message", "Unknown error")
            return None

        return response_json.get("data", [])

async def get_data(session:aiohttp.ClientSession)->dict:



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
                        params = make_params(TOKEN, CURRENCY, PAYMENT, ROLE, pages_count)
                        page_data = await fetch_page(session, BASE_URL, params)

                        pages_count += 1
                        await asyncio.sleep(PREFERENCES.UPDATE_RATE)
                        if not page_data:
                            continue

                        print(f"HTX---{ROLEN[ROLE]}---{CN[CURRENCY]}---{TN[TOKEN]}---{PN[PAYMENT]}---{pages_count}")
                        page_data = formed_data(page_data)
                        
                        result_data[ROLEN[ROLE]][CN[CURRENCY]][TN[TOKEN]][PN[PAYMENT]] += page_data
                        

    return result_data

def formed_data(data:dict) -> dict:
    result_data = []
    for i in range(len(data)):
        result_data.append({})
        try:
            result_data[i][USER_NAME] = data[i].get("userName")
            result_data[i][PRICE] = data[i].get("price")
            result_data[i][MIN_AMOUNT] = data[i].get("minTradeLimit")
            result_data[i][USER_ID] = data[i].get("userId")
            result_data[i][ADV_ID] = data[i].get("id")
        except Exception as e:
            print(">>>Unpack request data Exception:  " + str(e))
        return result_data


