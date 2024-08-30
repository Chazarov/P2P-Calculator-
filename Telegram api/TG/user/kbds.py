from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.types import FSInputFile, InputMediaPhoto, CallbackQuery
from aiogram.filters.callback_data import CallbackData

from TG.STATIC import P2P_PARS_URL, CALCULATOR_URL

from callbacks import USER_CALLBACKS as U_S

P2P_pars_web_app = WebAppInfo(url = P2P_PARS_URL)
Calculator_web_app = WebAppInfo(url = CALCULATOR_URL)


def main_menu_buttons():
    kbd = ReplyKeyboardMarkup(resize_keyboard = True, keyboard = [
            [
                KeyboardButton(text = "✅ Получить связки в приложении", web_app = P2P_pars_web_app),
            ],
            [
                KeyboardButton(text = "➕➖✖️ Калькулятор", web_app = Calculator_web_app),
            ],
        ]
    )
    return kbd

def sub_menu_buttons():
    kbd = InlineKeyboardMarkup(resize_keyboard = True, keyboard = [
            [
                InlineKeyboardButton(text = "💱 Узнать Курс валют", callback_data = U_S.EXCHANGE_RATE),
            ]
        ]
    )
    return kbd