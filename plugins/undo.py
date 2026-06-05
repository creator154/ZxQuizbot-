from pyrogram import filters
from database.mongo import quizzes

def register(app):

    @app.on_message(filters.command("undo"))
    async def undo(_, message):

        await message.reply_text(
            "↩ Last question removed."
        )

        # MongoDB pop logic yaha add karna hai
