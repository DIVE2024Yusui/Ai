from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

Key = 'api-key'
client = OpenAI(api_key=Key)
assistant_id = "assistant-key"

class Item(BaseModel):
    region: str
    mbti: List[str]
    num_people: List[int]
    
@app.post("/get_mission/")
async def create_item(data: Item):
    region = data.region
    
    # print(data.region, data.mbti, data.num_people)
    mbti_seq = ""
    for m,n in zip(data.mbti, data.num_people):
        mbti_seq += (m+str(n)+' ')
    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=f"{region} {mbti_seq}"
    )
    
    run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant_id
    )
    if run.status == 'completed': 
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        res = messages.data[0].content[0].text.value.split("\n")
        for idx, i in enumerate(res):
            if "1" in i:
                return res[idx:idx+5]
                
    else:
        return run.status

