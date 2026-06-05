From pyrogram import filters

quiz_states = {}

def register(app):

@app.on_message(filters.command("createquiz"))  
async def createquiz(_, message):  

    quiz_states[message.from_user.id] = {  
        "step": "title"  
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

        await message.reply_text(  
            "✅ Quiz Created\n\n"  
            "Now send Quiz Polls."  
        )  

        del quiz_states[user_id]
