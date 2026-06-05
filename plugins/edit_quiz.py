from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from bson import ObjectId
from database.mongo import quizzes

edit_state = {}


def register(app):

    @app.on_callback_query(filters.regex("^edit_"))
    async def edit_quiz(_, query):

        quiz_id = query.data.split("_", 1)[1]

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✏ Edit Title",
                        callback_data=f"edit_title_{quiz_id}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📝 Edit Description",
                        callback_data=f"edit_desc_{quiz_id}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🗑 Delete Quiz",
                        callback_data=f"delete_{quiz_id}"
                    )
                ]
            ]
        )

        await query.message.reply_text(
            "Select an option:",
            reply_markup=keyboard
        )

    @app.on_callback_query(filters.regex("^edit_title_"))
    async def edit_title(_, query):

        quiz_id = query.data.replace(
            "edit_title_",
            ""
        )

        edit_state[query.from_user.id] = {
            "type": "title",
            "quiz_id": quiz_id
        }

        await query.message.reply_text(
            "Send new title."
        )

    @app.on_callback_query(filters.regex("^edit_desc_"))
    async def edit_desc(_, query):

        quiz_id = query.data.replace(
            "edit_desc_",
            ""
        )

        edit_state[query.from_user.id] = {
            "type": "description",
            "quiz_id": quiz_id
        }

        await query.message.reply_text(
            "Send new description."
        )

    @app.on_message(filters.private & filters.text)
    async def edit_handler(_, message):

        user_id = message.from_user.id

        if user_id not in edit_state:
            return

        data = edit_state[user_id]

        quiz_id = data["quiz_id"]

        if data["type"] == "title":

            await quizzes.update_one(
                {
                    "_id": ObjectId(quiz_id)
                },
                {
                    "$set": {
                        "title": message.text
                    }
                }
            )

            await message.reply_text(
                "✅ Title Updated"
            )

        elif data["type"] == "description":

            await quizzes.update_one(
                {
                    "_id": ObjectId(quiz_id)
                },
                {
                    "$set": {
                        "description": message.text
                    }
                }
            )

            await message.reply_text(
                "✅ Description Updated"
            )

        del edit_state[user_id]
