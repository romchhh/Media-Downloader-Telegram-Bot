from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_admin_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text="Статистика", callback_data='user_statistic'),
        InlineKeyboardButton(text="Розсилка", callback_data='mailing')
    ]
    keyboard.add(*buttons)
    return keyboard


def get_back_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton("Назад", callback_data="adminback")
    keyboard.add(back_button)
    return keyboard


def get_preview_markup():
    markup = InlineKeyboardMarkup()
    preview_button = InlineKeyboardButton("📤 Надіслати", callback_data="send_broadcast")
    cancel_button = InlineKeyboardButton("❌ Відміна", callback_data="cancel_broadcast")
    markup.row(preview_button, cancel_button)
    markup.one_time_keyboard = True
    return markup
