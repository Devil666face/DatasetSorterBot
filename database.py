from pathlib import Path
import sqlite3
import aiosqlite
import os
from xmlrpc.client import Boolean
from aiogram import types

class Database:
    def __init__(self, db_file_name='database.db'):
        self.db_name = db_file_name
        self.connection = sqlite3.connect(db_file_name)
        self.cursor = self.connection.cursor()

    def create_user(self, message: types.Message):
        with self.connection:
            try:
                id = int(message.from_user.id)
                name = message.from_user.username
                self.cursor.execute(f"INSERT INTO User (id, name) VALUES ({id}, '{name}');")
                return True
            except Exception as error:
                print(f'[Ошибка добавления пользователя в БД] {error}')
                return False
            finally:
                self.connection.commit()

    def get_admin_id(self):
        with self.connection:
            self.cursor.execute(f"SELECT id FROM User WHERE admin=1")
            for id in self.cursor:
                return id
            return [0]

    def make_admin(self, id:int):
        with self.connection:
            try:
                if id not in self.get_admin_id():
                    self.cursor.execute(f"UPDATE User SET admin = 1 WHERE id={id};")
                else:
                    self.cursor.execute(f"UPDATE User SET admin = 0 WHERE id={id};")
                return True
            except Exception as error:
                print(f"[Ошибка изменения прав пользователя] невозможно изменить права id={id}.\n{error}")
                return False
            finally:
                self.connection.commit()

  
    async def add_photos_to_table(self, table_name, path_to_photo_folder):
        connection = await aiosqlite.connect(self.db_name)
        cursor = await connection.cursor()
        list_photo = os.listdir(path_to_photo_folder)
        try:
            for photo in list_photo:
                await self.add_photo(cursor, table_name, path_to_photo = str(Path(path_to_photo_folder,photo)))
        finally:
            await connection.commit()
            await connection.close()
            print('[Фото добавлены в базу]')

    async def add_photo(self, cursor, table_name, path_to_photo):
        try:
            await cursor.execute(f"INSERT INTO {table_name} (photo_path) VALUES (?)", (path_to_photo,))
        except Exception as error:
            print(f'[Ошибка добавления фото в базу] {error}')
            
    def clear_table(self, table_name):
        with self.connection:
            self.cursor.execute(f"DELETE FROM {table_name};")
            self.connection.commit()
            print(f"[Очистка таблицы с фото] таблица {table_name} очищена")

    def update_active_status(self, id, status:Boolean):
        with self.connection:
            self.cursor.execute(f"UPDATE User SET active = {int(status)} WHERE id={id};")
            self.connection.commit()

    def get_unsorted_photo(self):
        with self.connection:
            try:
                self.cursor.execute(f"SELECT photo_path FROM Photo WHERE sorted=0 LIMIT 1;")
                photo_path = self.cursor.fetchone()[0]
                self.cursor.execute(f"UPDATE Photo SET sorted=1  WHERE photo_path='{photo_path}';")
                self.connection.commit()
                return photo_path
            except Exception as error:
                print(f'[Ошибка выбора несортированного фото] {error}')
                return False

    def update_global_class(self, global_class_name, photo_id):
        with self.connection:
            self.cursor.execute(f"UPDATE Photo SET global_class='{global_class_name}'  WHERE id={photo_id};")
            self.connection.commit()

    def update_local_class(self, local_class_name, photo_id):
        with self.connection:
            self.cursor.execute(f"UPDATE Photo SET local_class='{local_class_name}'  WHERE id={photo_id};")
            self.connection.commit()

    def get_info_for_moving(self, photo_id):
        with self.connection:
            self.cursor.execute(f"SELECT photo_path, global_class, local_class FROM Photo WHERE id={photo_id};")
            return self.cursor.fetchone()

    def get_photo_id_by_path(self, photo_path):
        with self.connection:
            self.cursor.execute(f"SELECT id FROM Photo WHERE photo_path='{photo_path}'")
            return int(self.cursor.fetchone()[0])

    def get_photo_path_by_id(self, id):
        with self.connection:
            self.cursor.execute(f"SELECT photo_path FROM Photo WHERE id={id}")
            return str(self.cursor.fetchone()[0])

    def get_status(self, id):
        with self.connection:
            self.cursor.execute(f"SELECT active FROM User WHERE id={id}")
            return bool(self.cursor.fetchone()[0])
