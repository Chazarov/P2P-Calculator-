from django.conf import settings
import json
from pathlib import Path

from .ST_contexts.BASE_STATIC import PAYMENTS
from P2PCalculator.PREFERENCES import SM_DATA_FILE_NAME, KOEF_FILE_NAME

# сохранение будет производится в файл "STData.json" в динамической директории MEDIA <<< !!!

# Здесь нужно импортировать путь к сохраненному Json и производить поиск непосредственно в нем

# Шаблон json - запроса (Входящие данные): 
# params = {
#     "SM":""
#     "buy":{
#         "currency":"",
#         "token":"",
#         "min_amount":"",
#     },
#     "sell":{
#         "currency":"",
#         "token":"",
#         "min_amount":"",
#     }
# }

# Шаблон json - ответа (Выходящие данные): 
# request = {
#     "ceils":
#           {
#           "SM":"",
#           "buy":{
    #         "payment":"",
    #         "currency":"",
    #         "token":"",
    #         "min_amount":"",
    #       },
#           "sell":{
    #           "payment":"",
    #           "currency":"",
    #           "token":"",
    #           "min_amount":"",
    #           }
    #       },
#   }


# Итоговая сетка:
# 1 Raiffaizen=>Raiffaizen          2 Raiffaizen=>SBP          3 Raiffaizen=>SBER        4 Raiffaizen=>TINKOFF
# 5 SBP=>Raiffaizen                 6 SBP=>SBP                 7 SBP=>SBER               8 SBP=>TINKOFF
# 9 SBER=>Raiffaizen                10 SBER=>SBP               11 SBER=>SBER             12 SBER=>TINKOFF
# 13 TINKOFF=>Raiffaizen            14 TINKOFF=>SBP            15 TINKOFF=>SBER          16 TINKOFF=>TINKOFF

# Данные находятся в массиве по ключу ceils


# Checking the correctness of the request body
def check_fields(request):
    required_keys = {
        "SM": "",
        "buy": {
            "trade_role": "",
            "currency": "",
            "token": "",
            "min_amount": "",
        },
        "sell": {
            "trade_role": "",
            "currency": "",
            "token": "",
            "min_amount": "",
        }
    }


    def check_structure(d, structure):
        if not isinstance(d, dict) or not isinstance(structure, dict):
            return False

        for key, value in structure.items():
            if key not in d:
                return False
            if isinstance(value, dict):
                if not check_structure(d[key], value):
                    return False
        return True
    return check_structure(request, required_keys)





def processing_data(params:dict)->dict:
    
    if(not check_fields(params)): return None

    koefs_data = ""
    with open(Path(settings.MEDIA_ROOT).joinpath(KOEF_FILE_NAME), "r", encoding = "utf-8") as file:
        koefs_data = json.load(file)

    comission_buy = float(koefs_data.get(params["SM"]).get(params["buy"]["trade_role"]))
    comission_sell = float(koefs_data.get(params["SM"]).get(params["sell"]["trade_role"]))

    

    SM = params.get("SM")
    buy_block = params.get("buy")
    sell_block = params.get("sell")

    buy_min_amount = float(buy_block.get("min_amount"))
    sell_min_amount = float(sell_block.get("min_amount"))

    pars_data = None
    with open(Path(settings.MEDIA_ROOT).joinpath(SM_DATA_FILE_NAME), "r", encoding = "utf-8") as file:
        pars_data = json.load(file)

    buy_payments = pars_data.get(SM).get("BUY").get(buy_block["currency"]).get(buy_block["token"])
    sell_payments = pars_data.get(SM).get("BUY").get(sell_block["currency"]).get(sell_block["token"])

    

    PAYMENTS_LIST = PAYMENTS.to_list()
    best_offers = {payment:{} for payment in PAYMENTS_LIST}

    for PAYMENT in PAYMENTS_LIST:
        buy_filtered_offers = list(filter(lambda x: float(x['min_amount']) <= buy_min_amount, buy_payments[PAYMENT]))
        sell_filtered_offers = list(filter(lambda x: float(x['min_amount']) <= sell_min_amount, sell_payments[PAYMENT]))


        if(len(buy_filtered_offers) == 0): best_offers[PAYMENT]["buy"] = None
        else:best_offers[PAYMENT]["buy"] = max(buy_filtered_offers, key=lambda x: float(x["price"]))

        if(len(sell_filtered_offers) == 0): best_offers[PAYMENT]["sell"] = None
        else: best_offers[PAYMENT]["sell"] = min(sell_filtered_offers, key=lambda x: float(x["price"]))



    



    count = 0
    result_data = {}
    ceils = []
    for buy_idx in range(len(PAYMENTS_LIST)):
        for sell_idx in range(len(PAYMENTS_LIST)):


            buy_item = best_offers.get(PAYMENTS_LIST[buy_idx]).get("buy")
            sell_item = best_offers.get(PAYMENTS_LIST[sell_idx]).get("sell")

            if(buy_item == None or sell_item == None):
                ceil_data = {
                    "exists": "false"
                }
            else:
                
                buy_am = float(buy_item.get("price"))
                sell_am = float(sell_item.get("price"))

                buy_am = buy_am + buy_am*comission_buy
                sell_am = sell_am - sell_am*comission_sell
            
                koef = round(buy_am/sell_am, 2)


                ceil_data = {
                    "exists": "true",
                    "koef": str(koef),
                    "SM": SM,
                    "buy":{
                        "payment":PAYMENTS_LIST[buy_idx],
                        "currency":buy_block["currency"],
                        "token":buy_block["token"],
                        "min_amount":best_offers[PAYMENTS_LIST[buy_idx]]["buy"]["min_amount"],
                        "userName":best_offers[PAYMENTS_LIST[buy_idx]]["buy"]["user_name"],
                        "price":best_offers[PAYMENTS_LIST[buy_idx]]["buy"]["price"],
                    },
                    "sell":{
                        "payment":PAYMENTS_LIST[sell_idx],
                        "currency":sell_block["currency"],
                        "token":sell_block["token"],
                        "min_amount":best_offers[PAYMENTS_LIST[sell_idx]]["sell"]["min_amount"],
                        "userName":best_offers[PAYMENTS_LIST[sell_idx]]["sell"]["user_name"],
                        "price":best_offers[PAYMENTS_LIST[sell_idx]]["sell"]["price"],
                    },
                }
                ceils.append(ceil_data)
            count += 1

    result_data['ceils'] = ceils


    
    return result_data

