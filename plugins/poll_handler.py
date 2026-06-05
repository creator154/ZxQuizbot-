from pyrogram import filters
from database.mongo import quizzes

quiz_sessions = {}

def register(app):

    @app.on_poll()
    async def poll_update(_, poll):
        pass

    @app.on_message(filters.private & filters.poll)
    async def save_poll(_, message):

        user_id = message.from_user.id

        if user_id not in quiz_sessions:
            return

        quiz_id = quiz_sessions[user_id]

        question = {
            "question": message.poll.question,
            "options": [
                x.text for x in message.poll.options
            ],
            "answer": message.poll.correct_option_id
        }

        await quizzes.update_one(
            {"_id": quiz_id},
            {
                "$push": {
                    "questions": question
                }
            }
        )

        await message.reply_text(
            "✅ Question Added\n\n"
            "Send next poll or /done"
        )
