from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from motor.motor_asyncio import AsyncIOMotorClient

from config import *

app = Client(
    "ZxQuizBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

mongo = AsyncIOMotorClient(MONGO_URI)

db = mongo.ZxQuizBot

users = db.users
quizzes = db.quizzes


# ---------------- START ---------------- #

@app.on_message(filters.command("start"))
async def start(_, message):

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "➕ Create New Quiz",
                    callback_data="create_quiz"
                )
            ],
            [
                InlineKeyboardButton(
                    "📚 My Quizzes",
                    callback_data="my_quizzes"
                )
            ]
        ]
    )

    await message.reply_text(
        "👋 Welcome to ZxQuizBot\n\n"
        "Create and manage quizzes easily.",
        reply_markup=buttons
    )


# ---------------- CREATE QUIZ ---------------- #

quiz_states = {}


@app.on_callback_query(filters.regex("^create_quiz$"))
async def create_quiz(_, query):

    user_id = query.from_user.id

    quiz_states[user_id] = {
        "step": "title"
    }

    await query.message.reply_text(
        "📝 Send Quiz Title"
    )

    await query.answer()


@app.on_message(filters.private & filters.text)
async def title_handler(_, message):

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

        title = state["title"]
        description = message.text

        quiz = {
            "owner": user_id,
            "title": title,
            "description": description,
            "questions": [],
            "time_limit": None,
            "shuffle": False
        }

        result = await quizzes.insert_one(quiz)

        del quiz_states[user_id]

        await message.reply_text(
            f"✅ Quiz Created\n\n"
            f"Title: {title}\n"
            f"ID: {result.inserted_id}"
        )


# ---------------- MY QUIZZES ---------------- #

@app.on_callback_query(filters.regex("^my_quizzes$"))
async def my_quizzes(_, query):

    user_id = query.from_user.id

    data = quizzes.find(
        {"owner": user_id}
    )

    text = "📚 Your Quizzes\n\n"

    count = 0

    async for q in data:
        count += 1
        text += f"• {q['title']}\n"

    if count == 0:
        text = "❌ No quizzes found."

    await query.message.reply_text(text)

    await query.answer()


# ---------------- COMMANDS ---------------- #

@app.on_message(filters.command("createquiz"))
async def cmd_create(_, message):

    quiz_states[message.from_user.id] = {
        "step": "title"
    }

    await message.reply_text(
        "📝 Send Quiz Title"
    )


@app.on_message(filters.command("cancel"))
async def cancel(_, message):

    quiz_states.pop(
        message.from_user.id,
        None
    )

    await message.reply_text(
        "❌ Cancelled"
    )


print("ZxQuizBot Started...")

app.run()
