from pathlib import Path
import imghdr, os
from database import Database
from markup import Keyboards


class Controller:
    def __init__(self, DB:Database, KB:Keyboards, first_folder='military', second_folder='civil'):
        self.first_folder = Controller.get_std_path_to_dataset(first_folder)
        self.second_folder = Controller.get_std_path_to_dataset(second_folder)
        self.db = DB
        self.kb = KB
        print(self.first_folder, self.second_folder)

    @staticmethod
    def get_std_path_to_dataset(folder_name):
        if folder_name=='military' or folder_name=='civil':
            current_path = "/".join(map(str,__file__.split('/')[0:-1]))+f"/{folder_name}"
            return current_path
        return folder_name

    @staticmethod
    def remove_bad_photo(folder_path):
        image_extensions = [".png", ".jpg"]
        img_type_accepted_by_tf = ["bmp", "gif", "jpeg", "png"]
        for filepath in Path(folder_path).rglob("*"):
            if filepath.suffix.lower() in image_extensions:
                img_type = imghdr.what(filepath)
                if img_type is None:
                    os.remove(filepath)
                elif img_type not in img_type_accepted_by_tf:
                    os.remove(filepath)
        return f"[Удаление нечитаемых фото] директория {folder_path} очищена"
        
    def indexing_db(self):
        print(Controller.remove_bad_photo(self.first_folder)) #Удаляем не поддерживаемые расширения
        print(Controller.remove_bad_photo(self.second_folder))
        
        print(self.db.clear_table(table_name='Photo')) #Очищаем старые данные из таблицы

        self.db.add_photos_to_tables(table_name='Photo',folder_path=self.first_folder) #Заполняем таблицы 
        self.db.add_photos_to_tables(table_name='Photo',folder_path=self.second_folder)

        # self.db.create_updater_db_thread(table_name='Photo',folder_path=self.first_folder) #Заполняем таблицы 
        # self.db.create_updater_db_thread(table_name='Photo',folder_path=self.second_folder)

    def get_question(self):
        photo_path = self.db.get_unsorted_photo()
        keyboard_inline = self.kb.keyboard_create_inline_selector(photo_path)
        return photo_path, keyboard_inline

    def move_to_military(self, id):
        photo_path = self.db.get_photo_path_by_id(id)
        photo_name = photo_path.split('/')[-1]
        os.replace(photo_path,self.first_folder+photo_name)
        print(photo_path)

    def move_to_civil(self, id):
        photo_path = self.db.get_photo_path_by_id(id)
        photo_name = photo_path.split('/')[-1]
        os.replace(photo_path,self.second_folder+photo_name)
        print(photo_path)

    def delete(self, id):
        photo_path = self.db.get_photo_path_by_id(id)
        print(photo_path.split('/')[-1])
        os.remove(photo_path)

        