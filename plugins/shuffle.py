from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

def register(app):

    @app.on_callback_query(
        filters.regex("^shuffle_menu$")
    )
    async def shuffle_menu(_, query):

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Shuffle All",
                        callback_data="shuffle_all"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Shuffle Questions",
                        callback_data="shuffle_questions"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Shuffle Answers",
                        callback_data="shuffle_answers"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "No Shuffle",
                        callback_data="shuffle_none"
                    )
                ]
            ]
        )

        await query.message.reply_text(
            "Choose shuffle mode:",
            reply_markup=keyboard
        )
