import aiogram
from database import Database
from aiogram import types
from aiogram.types import ReplyKeyboardRemove,ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton
from aiogram.types.message import ContentTypes
from aiogram.types.message import ContentType

class Keyboards:
    def __init__(self, DB:Database):
        self.db = DB

    def keyboard_create_main_buttons(self, user_id):
        main_button = ['Начать выдачу','Остановить выдачу','Статистика','Помощь']
        if user_id in self.db.get_admin_id():
            main_button.append('Добавить фото в БД')
        keyboard_main = types.ReplyKeyboardMarkup(resize_keyboard=True) 
        keyboard_main.add(*main_button)
        return keyboard_main

    def keyboard_create_inline_selector(self, photo_path:str, first_folder='military', second_folder='civil', delete='delete'):
        id = self.db.get_photo_id_by_path(photo_path)
        inline_keyboard = types.InlineKeyboardMarkup()
        inline_keyboard.add(types.InlineKeyboardButton(text=f'{first_folder}',callback_data=f'inline_{first_folder}_{id}'))
        inline_keyboard.add(types.InlineKeyboardButton(text=f'{second_folder}',callback_data=f'inline_{second_folder}_{id}'))
        inline_keyboard.add(types.InlineKeyboardButton(text=f'{delete}',callback_data=f'inline_{delete}_{id}'))
        return inline_keyboard

    
