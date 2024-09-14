from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ParseMode
from aiogram.utils.exceptions import ChatNotFound
from main import bot, dp
from data.config import channel_id, administrators
from aiogram.dispatcher import Dispatcher
import asyncio
from filters.filters import IsSubscribed
from keyboards.user_keyboards import get_start_keyboard, get_comunity_keyboard, get_lang_keyboard, get_back, get_back_keyboard
from database.user_db import *
from functions.translate import translate_text
from states.user_states import SupportStates
from aiogram.dispatcher import FSMContext
from functions.user_functions import *
from aiogram.types import InputMediaPhoto, InputMediaVideo
import shutil
from functions.user_functions import VideoDownloader

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

    markup.add(InlineKeyboardButton(text=translate_text('Підписався', user.id), callback_data='check'))
    message_text = translate_text("Щоб отримати доступ до функцій бота, <b>потрібно підписатися на канал:</b>", user.id)

    if user_status.status == 'left':
        message_text = translate_text('❌ Ви не підписані!', user.id)
        await call.answer(message_text, show_alert=True)
        await call.message.edit_text(message_text, reply_markup=markup, disable_web_page_preview=True)
    else:
        message_text = translate_text('<b>✅ Успішно</b>', user.id)
        await call.message.edit_text(message_text)
        await asyncio.sleep(2)
        await call.message.edit_text(translate_text("Головне меню:", user.id), reply_markup=get_start_keyboard(user.id))

@dp.callback_query_handler(text="statystic")
async def handle_statistics(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id

    stats = get_statistics(user_id)
    
    if stats:
        statistics_text = (f"<b>Ваша статистика скачувань:</b>\n\n"
                           f"<b>Instagram:</b> {stats['instagram']} \n"
                           f"<b>TikTok:</b> {stats['tiktok']} \n"
                           f"<b>YouTube Shorts:</b> {stats['youtube']} \n"
                           f"<b>Pinterest:</b> {stats['pinterest']} ")
    else:
        statistics_text = "Статистика не знайдена."

    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text(statistics_text, parse_mode='HTML', reply_markup=get_back_keyboard(user_id))



@dp.callback_query_handler(text="help")
async def handle_help(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    
    help_text = (
        "<b>💡 Як користуватися ботом:</b>\n\n"
        "<b>1. Завантаження медіа:</b>\n"
        "Щоб завантажити медіа з соціальних мереж, надішліть посилання на пост або відео. "
        "Бот підтримує наступні платформи:\n"
        "  - Instagram\n"
        "  - TikTok\n"
        "  - YouTube Shorts\n"
        "  - Pinterest\n\n"
        "<b>2. Перегляд статистики:</b>\n"
        "Щоб переглянути вашу статистику скачувань, натисніть на кнопку 'Статистика'. "
        "Ви побачите, скільки медіа ви завантажили з кожної платформи.\n\n"
        "<b>📩 Є питання?:</b>\n"
        "Якщо у вас є питання або потрібна додаткова допомога, будь ласка, зв’яжіться з нами в Telegram: "
        "@TeleBotsNowayrm"
    )

    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text(help_text, parse_mode='HTML', reply_markup=get_back_keyboard(user_id))




@dp.callback_query_handler(IsSubscribed(), text="comunity")
async def handle_comunity(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    user_id = callback_query.from_user.id
    text = "Усі новини та актуальні канали команди TeleBotsNowayrm за посиланнями:"
    translated_text = translate_text(text, user_id)

    await callback_query.message.edit_text(translated_text, reply_markup=get_comunity_keyboard(user_id))


@dp.callback_query_handler(IsSubscribed(), text="download")
async def handle_download(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id

    text = "Будь ласка, надішліть посилання на медіа, яке ви хочете завантажити:"
    translated_text = translate_text(text, user_id)

    await callback_query.message.edit_text(translated_text, reply_markup=get_back(user_id))
    await SupportStates.waiting_for_media_link.set()

@dp.message_handler(state=SupportStates.waiting_for_media_link, content_types=types.ContentType.TEXT)
async def handle_media_link(message: types.Message, state: FSMContext):
    media_url = message.text
    user_id = message.from_user.id
    
    await bot.send_chat_action(message.chat.id, action="typing")

    # Check which social media platform the link belongs to
    if "instagram.com" in media_url:
        result = await download_media_from_instagram(media_url, user_id)
        update_downloads(user_id, 'instagram')  # Update the database
    elif "tiktok.com" in media_url:
        result = await download_media_from_tiktok(media_url, user_id)
        update_downloads(user_id, 'tiktok')  # Update the database
    elif "youtube.com/shorts" in media_url:
        video_downloader = VideoDownloader()
        result = await video_downloader.download_media_from_youtube_shorts(media_url, user_id)
    # подальша обробка result
        update_downloads(user_id, 'youtube')  # Update the database
    elif "pin.it" in media_url or "pinterest.com" in media_url:
        result = await download_media_from_pinterest(media_url, user_id)
        update_downloads(user_id, 'pinterest')  # Update the database
    else:
        await message.answer("Посилання не підтримується. Будь ласка, надішліть посилання з Instagram, TikTok, YouTube Shorts, Twitter або Pinterest.")
        return

    if result:
        directory = result.get('dir')
        caption = result.get('caption', '')
        files = result.get('files', [])
        is_video = result.get('is_video', False)
        
        if not files:
            await message.answer("Не вдалося знайти медіа файли для надсилання.")
            return
        
        if len(files) == 1:
            file_path = files[0]
            if file_path.endswith(".mp4"):
                with open(file_path, 'rb') as video:
                    await message.answer_video(video=video)
            elif file_path.endswith((".jpg", ".jpeg", ".png")) and not is_video:
                with open(file_path, 'rb') as photo:
                    await message.answer_photo(photo=photo)
        else:
            # Prepare media group if there are multiple files
            media_group = []
            for file_path in files:
                if file_path.endswith(".mp4"):
                    media_group.append(InputMediaVideo(open(file_path, 'rb')))
                elif file_path.endswith((".jpg", ".jpeg", ".png")):
                    media_group.append(InputMediaPhoto(open(file_path, 'rb')))
            
            if media_group:
                await message.answer_media_group(media_group)
                
        if caption:
            await message.answer(caption)

        shutil.rmtree(directory)
        await asyncio.sleep(2)
        await message.answer(translate_text("Головне меню:", user_id), reply_markup=get_start_keyboard(user_id))
    else:
        await message.answer("Не вдалося завантажити медіа за цим посиланням. Спробуйте ще раз.")

    await state.finish()

    
    
@dp.callback_query_handler(IsSubscribed(), text="settings")
async def handle_settings(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    user_id = callback_query.from_user.id
    language_keyboard = get_lang_keyboard(user_id)
    await callback_query.message.edit_text(
        translate_text("Оберіть мову інтерфейса:", user_id),
        reply_markup=language_keyboard
    )

@dp.callback_query_handler(lambda c: c.data.startswith("set_lang_"))
async def handle_language_selection(callback_query: CallbackQuery):
    lang = callback_query.data.split("_")[2]
    user_id = callback_query.from_user.id

    update_user_language(user_id, lang)

    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text(translate_text(f"Ви обрали мову: {'Українська' if lang == 'uk' else 'Англійська'}", user_id))
    await asyncio.sleep(2)
    await callback_query.message.edit_text(translate_text("Головне меню:", user_id), reply_markup=get_start_keyboard(user_id))


    
@dp.callback_query_handler(text="back")
async def handle_back(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    await callback_query.message.edit_text(translate_text("Головне меню:", user_id), reply_markup=get_start_keyboard(user_id))



@dp.callback_query_handler(IsSubscribed(), text="backck", state=SupportStates.waiting_for_media_link)
async def handle_back(callback_query: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    await callback_query.message.edit_text(translate_text("Головне меню:", user_id), reply_markup=get_start_keyboard(user_id))
    await state.finish()

    
def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(check, lambda c: c.data == 'check')

