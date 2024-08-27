import json
import os
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from django.core.handlers.wsgi import WSGIRequest

from django.conf import settings


from STPars.ST_contexts.Bitget.Static import SM_NAME as bitget_name
from STPars.ST_contexts.HTX.Static import SM_NAME as htx_name
from STPars.ST_contexts.Bybit.Static import SM_NAME as bybit_name

from P2PCalculator.PREFERENCES import KOEF_FILE_NAME

FILE_PATH = Path(settings.MEDIA_ROOT).joinpath(KOEF_FILE_NAME)

# Ожидаемые данные:
# data = {
#       
#     "BYBIT":{
#         "maker":koef/None,
#         "taker":koef/None,
#     },
#     "HTX":{
#         "maker":koef/None,
#         "taker":koef/None,
#     },
#     "BITGET":{
#         "maker":koef/None,
#         "taker":koef/None,
#     },
# }
#
#

RESPONCE_KEYS = {
        "BYBIT":{
            "maker":"",
            "taker":"",
        },
        "HTX":{
            "maker":"",
            "taker":"",
        },
        "BITGET":{
            "maker":"",
            "taker":"",
        },
    }



def check_fields(request, required_keys):

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






def refresh_koefs(request:WSGIRequest):

    data = json.loads(request.body)

    if(not check_fields(data, RESPONCE_KEYS)): 
        return None
    
    passw = os.getenv("SPECIAL_PASS")
    print(str(data.get("SPECIAL_PASS")) + "❗❗")
    if(data.get("SPECIAL_PASS") != passw): return "Invalid password"



    koefs_data = ""
    with open(Path(settings.MEDIA_ROOT).joinpath(KOEF_FILE_NAME), "r", encoding = "utf-8") as file:
        koefs_data = json.load(file)

    try:
        koefs_data["BYBIT"]["maker"] = str(float(data.get("BYBIT").get("maker")))
        koefs_data["BYBIT"]["taker"] = str(float(data.get("BYBIT").get("taker")))
        koefs_data["HTX"]["maker"] = str(float(data.get("HTX").get("maker")))
        koefs_data["HTX"]["taker"] = str(float(data.get("HTX").get("taker")))
        koefs_data["BITGET"]["maker"] = str(float(data.get("BITGET").get("maker")))
        koefs_data["BITGET"]["taker"] = str(float(data.get("BITGET").get("taker")))
    except ValueError as e:
        return "Value error"

    with open(Path(settings.MEDIA_ROOT).joinpath(KOEF_FILE_NAME), "w", encoding = "utf-8") as file:
        json.dump(koefs_data, file, ensure_ascii = False, indent = 4)

    return "Success"

    

def get_current_coefs():

    data = ""
    with open(Path(settings.MEDIA_ROOT).joinpath(KOEF_FILE_NAME), "r", encoding = "utf-8") as file:
        data = json.load(file)

    return data

    
    

