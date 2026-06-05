from pyrogram import filters
from database.quizzes import get_user_quizzes


def register(app):

    @app.on_callback_query(
        filters.regex("^my_quizzes$")
    )
    async def my_quizzes(_, query):

        data = await get_user_quizzes(
            query.from_user.id
        )

        if not data:

            return await query.message.reply_text(
                "❌ No quizzes found."
            )

        text = "📚 Your Quizzes\n\n"

        for q in data:
            text += f"• {q['title']}\n"

        await query.message.reply_text(text)
