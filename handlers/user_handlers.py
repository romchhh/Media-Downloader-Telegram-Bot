from main import bot, dp
from filters.filters import *
from aiogram import types

from keyboards.user_keyboards import get_start_keyboard, get_back
from keyboards.admin_keyboards import get_admin_keyboard
from database.user_db import *
from functions.translate import translate_text
from states.user_states import SupportStates
from aiogram.dispatcher import FSMContext


html = 'HTML'

async def antiflood(*args, **kwargs):
    m = args[0]
    await m.answer("Не поспішай :)")

async def on_startup(dp):
    # await scheduler_jobs()
    from handlers.user_handlers import dp as user_dp
    from callbacks.user_callbacks import register_callbacks
    from callbacks.admin_callbacks import register_admin_callbacks
    register_callbacks(dp)
    register_admin_callbacks(dp)
    me = await bot.get_me()
    print(f"Бот @{me.username} запущений!")

async def on_shutdown(dp):
    me = await bot.get_me()
    print(f'Bot: @{me.username} зупинений!')

@dp.message_handler(IsPrivate(), commands=["start"])
@dp.throttled(antiflood, rate=1)
async def start(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    user_first_name = message.from_user.first_name

    user = message.from_user
    keyboard = get_start_keyboard(user_id)
    add_user(user_id, user_name)
    
    start_text = (f"Привіт, {user.username}!\n"
    "Надішліть мені <b>посилання</b>, і я надішлю вам медіа!\n"
    "Зі мною ви можете завантажувати <b>фото</b> та <b>відео</b> з:\n\n"
    " <b>Instagram</b> (пости, reels)\n"
    " <b>TikTok</b>(Поки підтримує скачування лише відео)\n"
    " <b>YouTube Shorts</b>\n"
    " <b>Pinterest</b>(Поки підтримує скачування лише фото)\n\n"
    "Зв'язок: @TeleBotsNowayrm\n")

    greeting_message = translate_text(start_text, user_id)
    await message.answer(greeting_message, reply_markup=keyboard, disable_web_page_preview=True)


@dp.message_handler(commands=["download"], state="*")
async def handle_download(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    text = "Будь ласка, надішліть посилання на медіа, яке ви хочете завантажити:"
    translated_text = translate_text(text, user_id)

    await message.answer(translated_text, reply_markup=get_back(user_id))
    await SupportStates.waiting_for_media_link.set()

@dp.message_handler(IsPrivate(), commands=["admin"])
@dp.throttled(antiflood, rate=1)
async def admin_panel(message: types.Message):
    user = message.from_user
    if user.id in administrators:
        admin_keyboard = get_admin_keyboard()
        await message.answer("Адмін панель", reply_markup=admin_keyboard)
