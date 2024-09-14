from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, KeyboardButton, ContentTypes, ReplyKeyboardMarkup, \
    InputFile
    
from functions.translate import translate_text

def get_start_keyboard(user_id):
    keyboard = InlineKeyboardMarkup(row_width=2)

    buttons = [
        InlineKeyboardButton(text=translate_text("Скачати медіа", user_id), callback_data="download"),
    ]

    for button in buttons:
        keyboard.add(button)
        
    comunity_button = InlineKeyboardButton(text=translate_text("Ком'юніті", user_id), callback_data="comunity")
    statistic_button = InlineKeyboardButton(text=translate_text("Статистика", user_id), callback_data="statystic") 
    settings_button = InlineKeyboardButton(text=translate_text("Налаштування", user_id), callback_data="settings")
    help_button = InlineKeyboardButton(text=translate_text("Допомога", user_id), callback_data="help") 

    keyboard.row(comunity_button, statistic_button)
    keyboard.row(settings_button, help_button)

    return keyboard



def get_back_keyboard(user_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(translate_text("Назад", user_id), callback_data="back")
    keyboard.add(back_button)
    return keyboard



def get_back_statystic(user_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(translate_text("Назад", user_id), callback_data="statystic"))
    return keyboard

def get_comunity_keyboard(user_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    link_button_text = "Telegram"
    link2_button_text = "Instagram"
    link3_button_text = "Наша сторінка"
    back_button_text = translate_text("Назад", user_id)
    link_button = InlineKeyboardButton(text=link_button_text, url="https://t.me/TeleBotsNowayrmChannel")
    link2_button = InlineKeyboardButton(text=link2_button_text, url="https://www.instagram.com/telebotsnowayrm/")
    link3_button = InlineKeyboardButton(text=link3_button_text, url="https://romchhh.github.io/")
    back_button = InlineKeyboardButton(text=back_button_text, callback_data="back")
    keyboard.add(link_button, link2_button, link3_button, back_button)
    return keyboard



def get_back(user_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(translate_text("Назад", user_id), callback_data="backck"))
    return keyboard

def get_lang_keyboard(user_id):
    language_keyboard = InlineKeyboardMarkup(row_width=2)
    uk_button = InlineKeyboardButton(text=translate_text("Укр", user_id), callback_data="set_lang_uk")
    en_button = InlineKeyboardButton(text=translate_text("Англ", user_id), callback_data="set_lang_en")
    back_button = InlineKeyboardButton(text=translate_text("Назад", user_id), callback_data="back")
    language_keyboard.add(uk_button, en_button, back_button)
    return language_keyboard