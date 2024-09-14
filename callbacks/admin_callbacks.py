from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.exceptions import ChatNotFound
from main import bot, dp
from data.config import channel_id, administrators
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext

import asyncio
from keyboards.user_keyboards import get_start_keyboard
from keyboards.admin_keyboards import get_admin_keyboard, get_back_keyboard, get_preview_markup
from database.admin_db import get_users_count, get_all_user_ids
from filters.filters import IsAdmin
from states.admin_states import BroadcastState

import re

from aiogram.dispatcher.filters import Text

async def check(call: types.CallbackQuery):
    user = call.from_user
    markup = InlineKeyboardMarkup(row_width=1)
    try:
        ch_name = await bot.get_chat(channel_id)
        ch_link = ch_name.invite_link
        ch_name = ch_name.title
        button = InlineKeyboardButton(text=f'{ch_name}', url=ch_link)
        markup.add(button)
        user_status = await bot.get_chat_member(chat_id=channel_id, user_id=user.id)
    except ChatNotFound:
        for x in administrators:
            await bot.send_message(x, f'Бот видалений з каналу.')
        return

    markup.add(InlineKeyboardButton(text='Підписався', callback_data='check'))
    message_text = f"Щоб отримати доступ до функцій бота, <b>потрібно підписатися на канал:</b>"

    if user_status.status == 'left':
        message_text = '❌ Ви не підписані!'
        await call.answer(message_text, show_alert=True)
        await call.message.edit_text(message_text, reply_markup=markup, disable_web_page_preview=True)
    else:
        message_text = '<b>✅ Успішно</b>'
        await call.message.edit_text(message_text)
        await asyncio.sleep(2) 
        await call.message.edit_text("Головне меню:", reply_markup=get_start_keyboard()) 
    
@dp.callback_query_handler(IsAdmin(), text='user_statistic')
async def statistic_handler(callback_query: CallbackQuery):
    total_users = get_users_count()
    # active_users = get_active_users_count()

    response_message = (
            f"👥 Загальна кількість користувачів: {total_users}\n"
            # f"📱 Кількість активних користувачів: {active_users}\n"
        )
    
    keyboard = get_back_keyboard()
    await callback_query.message.edit_text(response_message, reply_markup=keyboard, parse_mode="HTML")

@dp.callback_query_handler(IsAdmin(), Text(startswith='mailing'))
async def send_broadcast_prompt(call: CallbackQuery):
    await call.message.answer("Будь ласка, введіть текст розсилки або натисніть /skip, щоб пропустити цей крок:")
    await BroadcastState.text.set()

@dp.message_handler(state=BroadcastState.text)
async def process_broadcast_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
    await message.answer("Будь ласка, відправте фото для включення в повідомлення або натисніть /skip, щоб пропустити цей крок:")
    await BroadcastState.photo.set()

@dp.message_handler(content_types=['photo'], state=BroadcastState.photo)
async def process_broadcast_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await message.answer("Будь ласка, введіть назву кнопки або натисніть /skip, щоб пропустити цей крок:")
    await BroadcastState.button_name.set()

@dp.message_handler(state=BroadcastState.button_name)
async def process_button_name(message: types.Message, state: FSMContext):
    if message.text == '/skip':
        async with state.proxy() as data:
            data['button_name'] = None
        await message.answer("Будь ласка, введіть URL для кнопки або натисніть /skip, щоб пропустити цей крок:")
        await BroadcastState.button_url.set()
    else:
        async with state.proxy() as data:
            data['button_name'] = message.text
        await message.answer("Будь ласка, введіть URL для кнопки або натисніть /skip, щоб пропустити цей крок:")
        await BroadcastState.button_url.set()

@dp.message_handler(state=BroadcastState.button_url)
async def process_button_url(message: types.Message, state: FSMContext):
    if message.text == '/skip':
        async with state.proxy() as data:
            data['button_url'] = None
        await send_preview(message.chat.id, data, state)
        await BroadcastState.preview.set()
    else:
        async with state.proxy() as data:
            data['button_url'] = message.text
        await send_preview(message.chat.id, data, state)
        await BroadcastState.preview.set()

async def send_preview(chat_id, data, state: FSMContext):
    preview_markup = InlineKeyboardMarkup()
    if 'button_name' in data and 'button_url' in data and data['button_name'] and data['button_url']:
        button = InlineKeyboardButton(text=data['button_name'], url=data['button_url'])
        preview_markup.add(button)

    text = "📣 *Попередній перегляд розсилки:*\n\n"
    text += data.get('text', '')

    if 'photo' in data and data['photo'] is not None:
        await bot.send_photo(chat_id, data['photo'], caption=text, parse_mode="Markdown", reply_markup=preview_markup)
    else:
        await bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=preview_markup)

    await bot.send_message(chat_id, "Все правильно?", reply_markup=get_preview_markup())

    async with state.proxy() as stored_data:
        stored_data.update(data)

@dp.callback_query_handler(text="send_broadcast", state=BroadcastState.preview)
async def send_broadcast_to_users_callback(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get('text', '')
    photo = data.get('photo')
    button_name = data.get('button_name')
    button_url = data.get('button_url')
    await send_broadcast_to_users(text, photo, button_name, button_url, call.message.chat.id)
    await call.answer()
    await state.finish()

@dp.message_handler(commands=['skip'], state=[BroadcastState.text, BroadcastState.photo, BroadcastState.button_name, BroadcastState.button_url])
async def skip_step(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'text' not in data:
            data['text'] = None
        if 'photo' not in data:
            data['photo'] = None
        if 'button_name' not in data:
            data['button_name'] = None
        if 'button_url' not in data:
            data['button_url'] = None

    current_state = await state.get_state()
    if current_state == BroadcastState.text.state:
        await BroadcastState.photo.set()
        await message.answer("Будь ласка, відправте фото для включення в повідомлення або натисніть /skip, щоб пропустити цей крок:")
    elif current_state == BroadcastState.photo.state:
        await BroadcastState.button_name.set()
        await message.answer("Будь ласка, введіть назву кнопки або натисніть /skip, щоб пропустити цей крок:")
    elif current_state == BroadcastState.button_name.state:
        await BroadcastState.button_url.set()
        await message.answer("Будь ласка, введіть URL для кнопки або натисніть /skip, щоб пропустити цей крок:")
    elif current_state == BroadcastState.button_url.state:
        await send_preview(message.chat.id, data, state)
        await BroadcastState.preview.set()

async def send_broadcast_to_users(text, photo, button_name, button_url, chat_id):
    try:
        user_ids = get_all_user_ids()
        for user_id in user_ids:
            if text.strip():
                try:
                    markup = InlineKeyboardMarkup()
                    if button_name and button_url:
                        button = InlineKeyboardButton(text=button_name, url=button_url)
                        markup.add(button)
                    if photo:
                        await bot.send_photo(user_id, photo, caption=text, parse_mode='HTML', reply_markup=markup)
                    else:
                        await bot.send_message(user_id, text, parse_mode='HTML', reply_markup=markup)
                except Exception as e:
                    print(f"Помилка при відправці повідомлення користувачу з ID {user_id}: {str(e)}")

        await bot.send_message(chat_id, f"Розсилка успішно відправлена {len(user_ids)} користувачам.")
        admin_keyboard = get_admin_keyboard()
        await bot.send_message(chat_id, "Панель адміністратора", reply_markup=admin_keyboard)
    except Exception as e:
        await bot.send_message(chat_id, f"Виникла помилка: {str(e)}")

@dp.callback_query_handler(text="cancel_broadcast", state=BroadcastState.preview)
async def cancel_broadcast_callback(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    await state.finish()
    await call.message.answer("Розсилка скасована.")
    admin_keyboard = get_admin_keyboard()
    await bot.send_message(user_id, "Панель адміністратора", reply_markup=admin_keyboard)
    await call.answer()

        
@dp.callback_query_handler(text="adminback")
async def handle_back(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    admin_keyboard = get_admin_keyboard()
    await callback_query.message.edit_text("Адмін панель", reply_markup=admin_keyboard)
    
def register_admin_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(check, lambda c: c.data == 'check')