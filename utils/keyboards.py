from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def start_keyboard():

    return InlineKeyboardMarkup(
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


def quiz_keyboard(quiz_id):

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "▶ Start Quiz",
                    callback_data=f"start_{quiz_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    "👥 Start In Group",
                    callback_data=f"group_start_{quiz_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    "✏ Edit Quiz",
                    callback_data=f"edit_{quiz_id}"
                )
            ]
        ]
    )
