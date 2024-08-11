
### РАБОЧАЯ ВЕРСИЯ

import asyncio

import openai
import time

import configparser

config = configparser.ConfigParser()
config.read("settings.ini")

openai.api_key = config["APIS"]["OPENAI_API"]

async def create_thread(ass_id, prompt):
    #assistant = openai.beta.assistants.retrieve(ass_id)

    thread = openai.beta.threads.create()
    my_thread_id = thread.id



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

async def run_oai(prompt):

    assistant_id = config["APIS"]["ASSISTENT_ID"]

    my_run_id, my_thread_id = await create_thread(assistant_id, prompt)

    status = await check_status(my_run_id, my_thread_id)

    while (status != "completed"):
        status = await check_status(my_run_id, my_thread_id)
        print(status)
        time.sleep(2)

    response = openai.beta.threads.messages.list(
    thread_id=my_thread_id
    )

    if response.data:
        print(response.data[0].content[0].text.value)


if __name__ == "__main__":
    while True:
        prompt = input("Запрос: ")
        if prompt == 'exit':
            break
        asyncio.run(run_oai(prompt))

