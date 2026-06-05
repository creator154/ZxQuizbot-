from pyrogram import filters
from bson import ObjectId
from database.mongo import quizzes


def register(app):

    @app.on_callback_query(
        filters.regex("^start_")
    )
    async def start_quiz(_, query):

        quiz_id = query.data.replace(
            "start_",
            ""
        )

        quiz = await quizzes.find_one(
            {
                "_id": ObjectId(quiz_id)
            }
        )

        if not quiz:
            return

        if not quiz["questions"]:
            return await query.message.reply_text(
                "Quiz has no questions."
            )

        q = quiz["questions"][0]

        await query.message.reply_poll(
            question=q["question"],
            options=q["options"],
            type="quiz",
            correct_option_id=q["answer"],
            open_period=quiz.get(
                "time_limit",
                15
            ),
            is_anonymous=False
        )
