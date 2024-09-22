import json
import os

from aiogram import F, types, Router, Bot
from aiogram.filters.command import Command
from aiohttp import ClientSession

from Contexts.Get_exchanges.Bitget.requests import get_single_ticker
from Contexts.Get_exchanges.CBR.requests import get_currency_rate_RUB
from Contexts.Get_exchanges.Blockchain.requests import get_curerncy_rate_BTC
from Contexts.Get_exchanges.STATIC import PAIRS_BITGET, CURRENCIES_BLOCKCHAIN_BTC, CURRENCIES_CBR_RUB

from TG.user.kbds import main_menu_buttons, sub_menu_buttons, exchange_rate_buttons

from TG.callbacks import USER_CALLBACKS, USER_REQUESTS


bot = Bot(token = os.getenv("TOKEN"))
router = Router()





@router.message(Command("start"))
async def command_start(message: types.Message):
    await message.answer("Добро пожаловать!", reply_markup = main_menu_buttons())
    await message.answer(text = " Выберите интересующий вариант по кнопкам ниже: ", reply_markup = sub_menu_buttons())



@router.message(F.text == USER_REQUESTS.MAIN_MENU)
async def main_menu(message: types.Message):
    await message.answer(text = " Выберите интересующий вариант по кнопкам ниже: ", reply_markup = sub_menu_buttons())
    await message.delete()



@router.message()
async def web_app_handler(web_responce:types.Message):

    data = json.loads(web_responce.web_app_data.data)

   
    koef = data["koef"]
    S_market = data["SM"]


    buy_username = data["buy"]["userName"]
    buy_payment = data["buy"]["payment"]
    buy_currency = data["buy"]["currency"]
    buy_token = data["buy"]["token"]
    buy_min_amount = data["buy"]["min_amount"]
    buy_price = data["buy"]["price"]
    buy_adv_id = data["buy"]["adv_id"]

    sell_username = data["sell"]["userName"]
    sell_payment = data["sell"]["payment"]
    sell_currency = data["sell"]["currency"]
    sell_token = data["sell"]["token"]
    sell_min_amount = data["sell"]["min_amount"]
    sell_price = data["sell"]["price"]
    sell_adv_id = data["sell"]["adv_id"]





    result = f"Связка {S_market} с коефициентом {koef}: \n"  +\
    f" >>> Покупка:\n"  +\
    f"    >> P2P Маркет {S_market} \n"  +\
    f"    >> У пользователя {sell_username}\n" +\
    f"    >> Слот На продажу {sell_token} за {sell_currency} по {sell_price}\n" +\
    f"    >> Оплата: {buy_payment}\n" +\
    f"    >> Минимальная стоимость: {sell_min_amount}₽ \n" +\
    f"    >> id Ордера: {buy_adv_id}\n\n" +\
    f" >>> Продажа:\n" +\
    f"    >> P2P Маркет {S_market} \n" +\
    f"    >> У пользователя {buy_username}\n" +\
    f"    >> Слот На покупку {buy_token} за {buy_currency} по {buy_price}\n" +\
    f"    >> Оплата: {sell_payment}\n" +\
    f"    >> Минимальная стоимость: {buy_min_amount}₽ \n" +\
    f"    >> id Ордера: {sell_adv_id}\n"


    await bot.send_message(web_responce.from_user.id, text = result)
    

@router.callback_query(F.data == USER_CALLBACKS.UPDATE_EXCHANGE_RATE)
@router.callback_query(F.data == USER_CALLBACKS.EXCHANGE_RATE)
async def exchange_rate(callback: types.CallbackQuery, session:ClientSession):

    async def edit_text(message:types.Message, text:str):
        if(message.text != text):
            await message.edit_text(text = text, reply_markup = exchange_rate_buttons())

    btcusdt = "-"
    rubusd = "-"
    btcusd = "-"

    btcusdt = await get_single_ticker(pair = PAIRS_BITGET.BTCUSDT ,session = session)
    text = (f" 💱Текущий курс: \n\n"+\
        f" ➡️ BTC/USDT: {btcusdt}\n"+\
        f" ➡️ RUB/USD: {rubusd}\n"+\
        f" ➡️ BTC/USD: {btcusd}\n")
    await edit_text(message = callback.message, text = text)

    rubusd = await get_currency_rate_RUB(char_code_currency = CURRENCIES_CBR_RUB.USD, session = session)
    text = (f" 💱Текущий курс: \n\n"+\
        f" ➡️ BTC/USDT: {btcusdt}\n"+\
        f" ➡️ RUB/USD: {rubusd}\n"+\
        f" ➡️ BTC/USD: {btcusd}\n")
    await edit_text(message = callback.message, text = text)
    
    btcusd = await get_curerncy_rate_BTC(char_code_currency = CURRENCIES_BLOCKCHAIN_BTC.USD, session = session)
    text = (f" 💱Текущий курс: \n\n"+\
        f" ➡️ BTC/USDT: {btcusdt}\n"+\
        f" ➡️ RUB/USD: {rubusd}\n"+\
        f" ➡️ BTC/USD: {btcusd}\n")
    await edit_text(message = callback.message, text = text)