from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def register(app):

    @app.on_message(filters.command("start"))
    async def start(_, message):

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ Create New Quiz",
                        callback_data="create_quiz"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📚 My Quizzes",
                        callback_data="my_quizzes"
                    )
                ]
            ]
        )

        await message.reply_text(
            "👋 Welcome to ZxQuizBot",
            reply_markup=keyboard
        )
