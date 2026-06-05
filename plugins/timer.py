from pyrogram import filters
from bson import ObjectId
from database.mongo import quizzes


def register(app):

    @app.on_callback_query(
        filters.regex("^time_")
    )
    async def set_time(_, query):

        seconds = int(
            query.data.split("_")[1]
        )

        quiz_id = query.message.reply_to_message.text

        await quizzes.update_one(
            {
                "_id": ObjectId(quiz_id)
            },
            {
                "$set": {
                    "time_limit": seconds
                }
            }
        )

        await query.message.reply_text(
            "✅ Time Saved\n\n"
            "Now select shuffle mode."
        )
