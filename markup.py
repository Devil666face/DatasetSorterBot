from database import Database
from aiogram import types
from aiogram.types import ReplyKeyboardRemove,ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton
from aiogram.types.message import ContentTypes
from aiogram.types.message import ContentType
from tree_dict import tree_dict, get_translate

class Keyboards:
    def __init__(self, DB:Database):
        self.db = DB

    def keyboard_create_main_buttons(self, user_id):
        # main_button = ['Начать выдачу','Остановить выдачу'] #Раскоментить если рекурсивная выдача
        main_button = ['Начать выдачу'] #Это закоментить
        if user_id in self.db.get_admin_id():
            main_button.append('Добавить фото в БД')
        keyboard_main = types.ReplyKeyboardMarkup(resize_keyboard=True) 
        keyboard_main.add(*main_button)
        return keyboard_main

    def create_global_selector(self, photo_path):
        id = self.db.get_photo_id_by_path(photo_path)
        inline_keyboard = types.InlineKeyboardMarkup()
        for key in tree_dict:
            inline_keyboard.add(types.InlineKeyboardButton(text=get_translate(key),callback_data=f'global_{key}_{id}'))
        return inline_keyboard

    def create_local_selector(self, id, global_class_name):
        inline_keyboard = types.InlineKeyboardMarkup()
        for item in tree_dict[global_class_name]:
            inline_keyboard.add(types.InlineKeyboardButton(text=get_translate(item),callback_data=f'local_{item}_{id}'))
        return inline_keyboard


    
