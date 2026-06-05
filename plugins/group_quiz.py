from pyrogram import filters
from bson import ObjectId
from database.mongo import quizzes


def register(app):

    @app.on_callback_query(
        filters.regex("^group_start_")
    )
    async def group_start(_, query):

        quiz_id = query.data.replace(
            "group_start_",
            ""
        )

        quiz = await quizzes.find_one(
            {
                "_id": ObjectId(quiz_id)
            }
        )

        if not quiz:
            return await query.message.reply_text(
                "Quiz not found."
            )

        await query.message.reply_text(
            f"📚 {quiz['title']}\n\n"
            f"Add bot to your group and "
            f"use /startquiz {quiz_id}"
        )

    @app.on_message(
        filters.command("startquiz")
        & filters.group
    )
    async def start_group_quiz(_, message):

        if len(message.command) < 2:
            return

        quiz_id = message.command[1]

        quiz = await quizzes.find_one(
            {
                "_id": ObjectId(quiz_id)
            }
        )

        if not quiz:
            return await message.reply_text(
                "Quiz not found."
            )

        await message.reply_poll(
            question=quiz["questions"][0]["question"],
            options=quiz["questions"][0]["options"],
            type="quiz",
            correct_option_id=quiz["questions"][0]["answer"],
            is_anonymous=False
        )
