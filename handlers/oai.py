
### РАБОЧАЯ ВЕРСИЯ

import openai
import time

from .database import Database

db = Database()

import configparser

config = configparser.ConfigParser()
config.read("settings.ini")

openai.api_key = config["APIS"]["OPENAI_API"]

assistant_id = config["APIS"]["ASSISTENT_ID"]

async def create_thread(ass_id, prompt, user_id):

    if not await db.check_user_in_db(user_id):


        thread = openai.beta.threads.create()
        my_thread_id = thread.id

        await db.create_user(user_id, my_thread_id)
    
    else:
        answer = await db.get_thread_id(user_id)
        try:
            my_thread_id = answer[0]
        except:
            print(answer)


    message = openai.beta.threads.messages.create(
        thread_id=my_thread_id,
        role="user",
        content=prompt
    )

    run = openai.beta.threads.runs.create(
        thread_id=my_thread_id,
        assistant_id=ass_id
    ) 

    run_id = run.id
    thread_id = my_thread_id

    return run_id, thread_id

async def check_status(run_id, thread_id):
    run = openai.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id,
    )
    return run.status

async def run_oai(prompt, user_id):

    my_run_id, my_thread_id = await create_thread(assistant_id, prompt, user_id)

    status = await check_status(my_run_id, my_thread_id)

    while (status != "completed"):
        status = await check_status(my_run_id, my_thread_id)
        print(status)
        time.sleep(2)

    response = openai.beta.threads.messages.list(
    thread_id=my_thread_id
    )

    if response.data:
        print(response.data[0])
        return response.data[0].content[0].text.value




