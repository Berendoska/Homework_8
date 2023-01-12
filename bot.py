from aiogram import types, executor, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from Tok import TOKEN
from sq import bedin_database, create_contact, edit_contact


async def on_startup(_):
    await bedin_database()


storage = MemoryStorage()
bot = Bot(TOKEN)
dp = Dispatcher(bot,
                storage=storage)


class PeopleStatesGroup(StatesGroup):

    phone = State()
    name = State()
    surname = State()
    comment = State()


def get_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/create'))

    return kb

def get_cancel_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/cancel'))

    return kb


@dp.message_handler(commands=['cancel'], state='*')
async def cmd_cancel(message: types.Message, state: FSMContext):
    if state is None:
        return

    await state.finish()
    await message.reply('Вы прервали создание контакта!',
                        reply_markup=get_kb())


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    await message.answer('Привет! Добавь новый контакт  - type /create',
                         reply_markup=get_kb())

    await create_contact(phone=message.from_user.id)


@dp.message_handler(commands=['create'])

async def cmd_create(message: types.Message) -> None:   
#     await message.reply("Let's create your profile! To begin with, send me your photo!",
#                         reply_markup=get_cancel_kb())
#     await ProfileStatesGroup.photo.set()  # установили состояние фото


# @dp.message_handler(lambda message: not message.photo, state=ProfileStatesGroup.photo)
# async def check_photo(message: types.Message):
#     await message.reply('Это не фотография!')


# @dp.message_handler(content_types=['photo'], state=ProfileStatesGroup.photo)
# async def load_photo(message: types.Message, state: FSMContext) -> None:
#     async with state.proxy() as data:
#         data['photo'] = message.photo[0].file_id

    await message.reply('Введите имя!')
    await PeopleStatesGroup.next()



@dp.message_handler(state=PeopleStatesGroup.name)
async def load_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['name'] = message.text

    await message.reply('Введите реальный номер телефона не больше 8 знаков')
    await PeopleStatesGroup.next()


@dp.message_handler(state=PeopleStatesGroup.phone)
async def load_phone(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['phone'] = message.text

    await message.reply('Введите фамилию')
    await PeopleStatesGroup.next()


@dp.message_handler(state=PeopleStatesGroup.surname)
async def load_surn(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['surname'] = message.text
        # await bot.send_photo(chat_id=message.from_user.id,
        #                       phone=data['phone'],
        #                       caption=f"{data['name']}, {data['surname']}\n{data['comment']}")
    await message.reply('Комментарий')
    await PeopleStatesGroup.next()

@dp.message_handler(state=PeopleStatesGroup.comment)
async def load_comment(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['comment'] = message.text

    await edit_contact(state, phone=message.from_user.id)
    await message.reply('Ваша акнета успешно создана!')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)