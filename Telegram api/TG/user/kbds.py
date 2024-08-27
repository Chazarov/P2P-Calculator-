from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.types import FSInputFile, InputMediaPhoto, CallbackQuery
from aiogram.filters.callback_data import CallbackData

from TG.STATIC import BYBIT_URL

Bybit_web_app = WebAppInfo(url = BYBIT_URL)


def menu_buttons():
    kbd = ReplyKeyboardMarkup(resize_keyboard = True, keyboard = [
            [
                KeyboardButton(text = "✅Получить связки в приложении", web_app = Bybit_web_app),
            ],
        ]
    )
    return kbd