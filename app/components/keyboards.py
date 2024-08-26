# create keyboard
from aiogram.types import (ReplyKeyboardMarkup,KeyboardButton,
                           InlineKeyboardMarkup,InlineKeyboardButton)

from aiogram.utils.keyboard import InlineKeyboardBuilder

        # Создаем сборщика клавиатур типа Reply
start_keyboard= ReplyKeyboardMarkup(keyboard=[
    # Добавляем в сборщик одну кнопку
    [KeyboardButton(text="Начать игру")]
],
                          resize_keyboard=True, 
                          input_field_placeholder='choice item menu') 


def generate_options_keyboard(answer_options):
    builder = InlineKeyboardBuilder()

    for index, option in enumerate(answer_options['options']):
        callback_data = f"answer_{answer_options['correct_option'][index]}"    
        builder.add(InlineKeyboardButton(
            text = f"{option}",
            callback_data = callback_data
        ))

    builder.adjust(1)
    return builder.as_markup()


def create_confirmation_keyboard():
    keyboard = InlineKeyboardMarkup()  
    confirm_button = InlineKeyboardButton("Да", callback_data="confirm_yes")
    cancel_button = InlineKeyboardButton("Нет", callback_data="confirm_no")
    keyboard.add(confirm_button, cancel_button) 
    return keyboard

confirmation_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Да", callback_data="confirm_yes")],
    [InlineKeyboardButton(text="Нет", callback_data="confirm_no")]
])


