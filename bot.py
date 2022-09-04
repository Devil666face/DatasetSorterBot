import config
from aiogram import Bot,Dispatcher,types,executor
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from controller import Controller
from database import Database
from markup import Keyboards

bot = Bot(token=config.TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)

db = Database(db_file_name='database.db')
kb = Keyboards(db)
controller = Controller(db, kb)

@dp.message_handler(commands = ['make_admin'],state=None)
async def make_admin(message: types.Message):
    if db.make_admin(int(message.text.split()[1])):
        await message.answer(f'Права пользователя {int(message.text.split()[1])} изменены',reply_markup=kb.keyboard_create_main_buttons(message.from_user.id))
    else:
        await message.answer(f'Невозможно изменение прав пользователя {int(message.text.split()[1])}',reply_markup=kb.keyboard_create_main_buttons(message.from_user.id))
    

@dp.message_handler(commands = ['start'],state=None)
async def start(message: types.Message):
    if db.create_user(message=message):
        await message.answer(f'Вы добавлены в пользователи\nid = {message.from_user.id}\nname = {message.from_user.username}\nadmin = 0',reply_markup=kb.keyboard_create_main_buttons(message.from_user.id))
    else:
        await message.answer(f'Пользователь уже создан',reply_markup=kb.keyboard_create_main_buttons(message.from_user.id))


@dp.message_handler(Text(equals='Добавить фото в БД'))
async def indexing_db(message: types.Message, state: FSMContext):
    if message.from_user.id in db.get_admin_id():
        await message.answer('Начинаю добавление новых фото в БД. Процесс займет много времени.',reply_markup=kb.keyboard_create_main_buttons(message.from_user.id))
        await message.answer('Успешно.') if controller.add_path_to_db() else await message.answer('Ошибка обновления базы.')   
    else:
        await message.answer('У вас недостаточно прав для выполенния данных действий',reply_markup=kb.keyboard_create_main_buttons(message.from_user.id))


@dp.message_handler(Text(equals='Начать выдачу'))
async def get_photo(message: types.Message, state: FSMContext):
    db.update_active_status(id=message.from_user.id,status=True)
    for i in range(10): #Закоментить если рекурсивная выдача
        await get_global_question(message.from_user.id)

async def get_global_question(user_id):
    if db.get_status(user_id):
        photo_path, keyboard_inline = controller.get_global_question()
        await bot.send_photo(user_id, open(photo_path,'rb'),reply_markup=keyboard_inline) if photo_path else False
            
@dp.callback_query_handler(text_contains="global_")
async def set_global_class(call: types.CallbackQuery):
    class_name, photo_id =get_class_and_id(call.data)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    # Если вернет имя глобального класса - задаем еще один вопрос и опередляем локальный класс 
    global_class_name = controller.update_global_class(class_name, photo_id)
    if global_class_name:
        await get_local_question(call.from_user.id, photo_id, global_class_name)
    else:
        # Вернулся False поэтому делаем рекурсию и задаем следующий глобальный вопрос для этого же фото
        # Распределяем фото в нужную папку
        controller.move_photo(photo_id)
        # await get_global_question(call.from_user.id) #Рекурсия 

async def get_local_question(user_id, photo_id, global_class_name):
    photo_path, keyboard_inline = controller.get_local_question(photo_id, global_class_name)
    await bot.send_photo(user_id, open(photo_path,'rb'),reply_markup=keyboard_inline) if photo_path else False
        

@dp.callback_query_handler(text_contains="local_")
async def set_local_class(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    class_name, photo_id =get_class_and_id(call.data)
    controller.update_local_class(class_name,photo_id)
    # Распределяем фото в нужную папку
    controller.move_photo(photo_id)
    # Рекурсивно сново задаем глобальный вопрос
    # await get_global_question(call.from_user.id) #Рекурсия

@dp.message_handler(Text(equals='Остановить выдачу'))
async def help(message: types.Message, state: FSMContext):
    db.update_active_status(id=message.from_user.id,status=False)
    await message.answer('Выдача остановлена',reply_markup=kb.keyboard_create_main_buttons(message.from_user.id))

@dp.message_handler(content_types=['text'],state=None)
async def not_response(message: types.Message, state:FSMContext):
    await message.answer('Я вас не понимаю',reply_markup=kb.keyboard_create_main_buttons(message.from_user.id))

def get_class_and_id(call_data):
    return call_data.split('_')[1], call_data.split('_')[2]

if __name__=='__main__':
    executor.start_polling(dp, skip_updates=True)

