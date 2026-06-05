from pyrogram import filters

quiz_states = {}


def register(app):

    @app.on_message(filters.command("createquiz"))
    async def createquiz(_, message):

        quiz_states[message.from_user.id] = {
            "step": "title",
            "title": "",
            "description": "",
            "questions": []
        }

        await message.reply_text(
            "📝 Send Quiz Title"
        )

    @app.on_message(filters.private & filters.text)
    async def quiz_flow(_, message):

        user_id = message.from_user.id

        if user_id not in quiz_states:
            return

        state = quiz_states[user_id]

        if state["step"] == "title":

            state["title"] = message.text
            state["step"] = "description"

            await message.reply_text(
                "📄 Send Quiz Description"
            )
            return

        if state["step"] == "description":

            state["description"] = message.text
            state["step"] = "polls"

            await message.reply_text(
                "📊 Send Quiz Polls\n\n"
                "Send Telegram Quiz Polls one by one.\n\n"
                "/done - Finish Quiz\n"
                "/undo - Remove Last Question"
            )
            return

    @app.on_message(filters.private & filters.poll)
    async def save_poll(_, message):

        user_id = message.from_user.id

        if user_id not in quiz_states:
            return

        state = quiz_states[user_id]

        if state["step"] != "polls":
            return

        if not message.poll.quiz:
            return await message.reply_text(
                "❌ Send a Quiz Poll, not a regular poll."
            )

        question = {
            "question": message.poll.question,
            "options": [x.text for x in message.poll.options],
            "answer": message.poll.correct_option_id
        }

        state["questions"].append(question)

        await message.reply_text(
            f"✅ Question Added\n"
            f"Total Questions: {len(state['questions'])}"
        )

    @app.on_message(filters.command("undo"))
    async def undo(_, message):

        user_id = message.from_user.id

        if user_id not in quiz_states:
            return

        state = quiz_states[user_id]

        if not state["questions"]:
            return await message.reply_text(
                "❌ No questions to remove."
            )

        state["questions"].pop()

        await message.reply_text(
            "↩ Last Question Removed"
        )

    @app.on_message(filters.command("done"))
    async def done(_, message):

        user_id = message.from_user.id

        if user_id not in quiz_states:
            return

        state = quiz_states[user_id]

        if len(state["questions"]) == 0:
            return await message.reply_text(
                "❌ Add at least one Quiz Poll."
            )

        await message.reply_text(
            f"✅ Quiz Created\n\n"
            f"📚 Title: {state['title']}\n"
            f"📄 Description: {state['description']}\n"
            f"❓ Questions: {len(state['questions'])}"
        )

        del quiz_states[user_id]
