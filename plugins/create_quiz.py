from pyrogram import filters

quiz_data = {}

def register(app):

    @app.on_message(filters.command("createquiz"))
    async def createquiz(_, message):

        quiz_data[message.from_user.id] = {
            "step": "title",
            "title": "",
            "description": "",
            "question": "",
            "options": [],
            "correct": None
        }

        await message.reply_text("📝 Send Quiz Title")

    @app.on_message(filters.private & ~filters.command("createquiz"))
    async def quiz_flow(_, message):

        user_id = message.from_user.id

        if user_id not in quiz_data:
            return

        state = quiz_data[user_id]

        # STEP 1: TITLE
        if state["step"] == "title":
            state["title"] = message.text
            state["step"] = "description"
            return await message.reply_text("📘 Send Quiz Description")

        # STEP 2: DESCRIPTION
        if state["step"] == "description":
            state["description"] = message.text
            state["step"] = "question"
            return await message.reply_text("❓ Send Question")

        # STEP 3: QUESTION
        if state["step"] == "question":
            state["question"] = message.text
            state["step"] = "options"
            return await message.reply_text(
                "📌 Send 4 options one by one"
            )

        # STEP 4: OPTIONS
        if state["step"] == "options":
            state["options"].append(message.text)

            if len(state["options"]) < 4:
                return await message.reply_text(
                    f"✅ Option added ({len(state['options'])}/4)"
                )

            state["step"] = "correct"
            return await message.reply_text("🎯 Send correct option number (1-4)")

        # STEP 5: CORRECT + SEND POLL
        if state["step"] == "correct":
            try:
                correct_index = int(message.text) - 1

                if correct_index not in [0,1,2,3]:
                    return await message.reply_text("❌ Only 1-4 allowed")

                state["correct"] = correct_index

                # 📌 TITLE + DESCRIPTION MESSAGE (official feel)
                await message.reply_text(
                    f"📚 {state['title']}\n"
                    f"📝 {state['description']}"
                )

                # 📊 QUIZ POLL SEND
                await message.reply_poll(
                    question=state["question"],
                    options=state["options"],
                    type="quiz",
                    correct_option_id=state["correct"],
                    is_anonymous=False
                )

                await message.reply_text("✅ Quiz Created Successfully!")

                del quiz_data[user_id]

            except:
                await message.reply_text("❌ Send valid number (1-4)")
