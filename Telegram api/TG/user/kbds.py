from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.types import FSInputFile, InputMediaPhoto, CallbackQuery
from aiogram.filters.callback_data import CallbackData

from TG.STATIC import P2P_PARS_URL, CALCULATOR_URL

from TG.callbacks import USER_CALLBACKS as U_S, USER_REQUESTS as U_R

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
            [
                KeyboardButton(text = U_R.MAIN_MENU),
            ],
        ]
    )
    return kbd



def sub_menu_buttons():
    kbd = InlineKeyboardMarkup(inline_keyboard = [
            [
                InlineKeyboardButton(text = "💱 Узнать Курс валют", callback_data = U_S.EXCHANGE_RATE),
            ]
        ]
    )
    return kbd



def exchange_rate_buttons():
    kbd = InlineKeyboardMarkup(inline_keyboard = [
            [
                InlineKeyboardButton(text = "🔄Обновить🔄", callback_data = U_S.UPDATE_EXCHANGE_RATE),
            ]
        ])
    
    return kbd