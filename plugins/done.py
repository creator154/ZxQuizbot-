from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

def register(app):

    @app.on_message(filters.command("done"))
    async def done(_, message):

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "10 sec",
                        callback_data="time_10"
                    ),
                    InlineKeyboardButton(
                        "15 sec",
                        callback_data="time_15"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "30 sec",
                        callback_data="time_30"
                    )
                ]
            ]
        )

        await message.reply_text(
            "Select time limit:",
            reply_markup=keyboard
        )
