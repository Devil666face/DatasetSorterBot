from pathlib import Path
import imghdr, os
from database import Database
from markup import Keyboards
from sys import platform


class Controller:
    def __init__(self, DB:Database, KB:Keyboards):
        self.db = DB
        self.kb = KB
        self.Not_sorted = Path(os.getcwd(),'Dataset','NotSorted')
        
    async def add_path_to_db(self):
        try:
            self.remove_bad_photo(self.Not_sorted)
            self.db.clear_table(table_name='Photo')
            await self.db.add_photos_to_table(table_name='Photo',path_to_photo_folder=self.Not_sorted)
            return True
        except Exception as error:
            print(f"[Ошибка заполнения базы данных] {error}")
            return False
  
    def get_global_question(self):
        photo_path = self.db.get_unsorted_photo()
        return photo_path, self.kb.create_global_selector(photo_path)

    def update_global_class(self, class_name, photo_id):
        self.db.update_global_class(class_name,photo_id)
        return class_name if class_name in ['Allowed','NotAllowed','Vehicles'] else False

    def get_local_question(self, photo_id, global_class_name):
        return self.db.get_photo_path_by_id(photo_id), self.kb.create_local_selector(photo_id, global_class_name)

    def update_local_class(self, class_name, photo_id):
        self.db.update_local_class(class_name,photo_id)

    def move_photo(self, photo_id):
        photo_info_list = self.db.get_info_for_moving(photo_id=photo_id)
        photo_name = self.get_photo_name(photo_info_list[0])
        if photo_info_list[1]=='Delete':
            os.remove(photo_info_list[0])
            return True
        if photo_info_list[2]=='none':
            os.replace(photo_info_list[0],Path(os.getcwd(),'Dataset','Sorted',photo_info_list[1],photo_name))
            return True
        os.replace(photo_info_list[0],Path(os.getcwd(),'Dataset','Sorted',photo_info_list[1],photo_info_list[2],photo_name))
        return True

    def get_photo_name(self, photo_path):
        if platform == "linux" or platform == "linux2":
            return photo_path.split('/')[-1]
        elif platform == "win32":
            return photo_path.split('\\')[-1]

    def remove_bad_photo(self, folder_path):
        try:
            image_extensions = [".png", ".jpg"]
            img_type_accepted_by_tf = ["bmp", "gif", "jpeg", "png"]
            for filepath in Path(folder_path).rglob("*"):
                if filepath.suffix.lower() in image_extensions:
                    img_type = imghdr.what(filepath)
                    if img_type is None:
                        os.remove(filepath)
                    elif img_type not in img_type_accepted_by_tf:
                        os.remove(filepath)
            print(f"[Удаление нечитаемых фото] директория {folder_path} очищена")
            return True
        except Exception as error:
            print(f"[Ошибка очистки директории от неподдерживаемых фото] {error}")
            return False

    # def move_to_military(self, id):
    #     photo_path = self.db.get_photo_path_by_id(id)
    #     photo_name = photo_path.split('/')[-1]
    #     os.replace(photo_path,self.first_folder+photo_name)
    #     print(f"[Изменение фото] {photo_path} перемещено в military")

    # def move_to_civil(self, id):
    #     photo_path = self.db.get_photo_path_by_id(id)
    #     photo_name = photo_path.split('/')[-1]
    #     os.replace(photo_path,self.second_folder+photo_name)
    #     print(f"[Изменение фото] {photo_path} перемещено в civil")

    # def delete(self, id):
    #     photo_path = self.db.get_photo_path_by_id(id)
    #     os.remove(photo_path)
    #     print(f"[Изменение фото] {photo_path} удалено")