import sqlite3, os
from types import NoneType
from xmlrpc.client import Boolean
from aiogram import types
from threading import Thread

class Database:
    def __init__(self, db_file_name='database.db'):
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

    # def create_updater_db_thread(self, table_name, folder_path:str):
    #     thread = Thread(target=self.add_photos_to_tables, args=[table_name,folder_path])
    #     thread.start()


    def add_photos_to_tables(self, table_name, folder_path:str):
        photos = os.listdir(folder_path)
        with self.connection:
            for (i,photo) in enumerate(photos):
                try:
                    self.cursor.execute(f"INSERT INTO {table_name} (photo_path) VALUES ('{folder_path+photo}');")
                    print(f"[{i+1}/{len(photos)}] {folder_path+photo} - добавлен")
                except Exception as error:
                    print(f'[Ошибка добавления фото в базу] {error}')

                finally:
                    self.connection.commit()
            
    def clear_table(self, table_name):
        self.cursor.execute(f"DELETE FROM {table_name};")
        self.connection.commit
        return f"[Очистка таблицы с фото] таблица {table_name} очищена"

    def update_active_status(self, id, status:Boolean):
        self.cursor.execute(f"UPDATE User SET active = {int(status)} WHERE id={id};")
        self.connection.commit()

    def get_unsorted_photo(self):
        try:
            self.cursor.execute(f"SELECT photo_path FROM Photo WHERE sorted=0 LIMIT 1;")
            photo_path = self.cursor.fetchone()[0]
            self.cursor.execute(f"UPDATE Photo SET sorted=1  WHERE photo_path='{photo_path}';")
            self.connection.commit()
            return photo_path
            
        except Exception as error:
            print(f'[Ошибка выбора несортированного фото] {error}')
            return False

    def get_photo_id_by_path(self, photo_path):
        self.cursor.execute(f"SELECT id FROM Photo WHERE photo_path='{photo_path}'")
        return int(self.cursor.fetchone()[0])

    def get_photo_path_by_id(self, id):
        self.cursor.execute(f"SELECT photo_path FROM Photo WHERE id={id}")
        return str(self.cursor.fetchone()[0])

    def get_status(self, id):
        self.cursor.execute(f"SELECT active FROM User WHERE id={id}")
        return bool(self.cursor.fetchone()[0])