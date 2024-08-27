import json
import os

from aiogram import F, types, Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile, InputMediaPhoto, CallbackQuery, WebAppInfo
from aiogram.fsm.context import FSMContext

from aiogram.utils.web_app import safe_parse_webapp_init_data
from aiohttp.web_request import Request
from aiohttp.web_response import json_response, Response

from TG.user.kbds import menu_buttons
from TG.STATIC import BYBIT_URL


bot = Bot(token = os.getenv("TOKEN"))
router = Router()


Bybit_web_app = WebAppInfo(url = BYBIT_URL)



@router.message(Command("start"))
async def command_start(message: types.Message):
    await message.answer("Главное меню", reply_markup = menu_buttons())


@router.message()
async def web_app_handler(web_responce:types.Message):

    data = json.loads(web_responce.web_app_data.data)
    print(data)

   
    koef = data["koef"]
    S_market = data["SM"]


    buy_username = data["buy"]["userName"]
    buy_payment = data["buy"]["payment"]
    buy_currency = data["buy"]["currency"]
    buy_token = data["buy"]["token"]
    buy_min_amount = data["buy"]["min_amount"]
    buy_price = data["buy"]["price"]

    sell_username = data["sell"]["userName"]
    sell_payment = data["sell"]["payment"]
    sell_currency = data["sell"]["currency"]
    sell_token = data["sell"]["token"]
    sell_min_amount = data["sell"]["min_amount"]
    sell_price = data["sell"]["price"]





    result = f"Связка {S_market} с коефициентом {koef}: \n"  +\
    f" >>>Покупка:\n"  +\
    f"    >>P2P Маркет {S_market} \n"  +\
    f"    >>У пользователя {sell_username}\n" +\
    f"    >>Слот На продажу {sell_token} за {sell_currency} по {sell_price}\n" +\
    f"    >>Минимальная стоимость: {sell_min_amount}\n\n" +\
    f" >>>Продажа:\n" +\
    f"    >>P2P Маркет {S_market} \n" +\
    f"    >>У пользователя {buy_username}\n" +\
    f"    >>Слот На покупку {buy_token} за {buy_currency} по {buy_price}\n" +\
    f"    >>Минимальная стоимость: {buy_min_amount}\n"

    await bot.send_message(web_responce.from_user.id, text = result)
    

