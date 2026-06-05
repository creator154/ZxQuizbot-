from .mongo import quizzes


async def create_quiz(data):

    return await quizzes.insert_one(
        data
    )


async def get_quiz(quiz_id):

    return await quizzes.find_one(
        {"_id": quiz_id}
    )


async def get_user_quizzes(user_id):

    result = []

    async for q in quizzes.find(
        {"owner": user_id}
    ):
        result.append(q)

    return result


async def delete_quiz(quiz_id):

    return await quizzes.delete_one(
        {"_id": quiz_id}
    )
