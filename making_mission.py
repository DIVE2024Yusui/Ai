from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

Key = 'user_key'
client = OpenAI(api_key=Key)
assistant_id = "assistant_key"

class Item(BaseModel):
    region: str = ""
    mbti: List[str]
    num_people: List[int]

class Question(BaseModel):
    mission: str
    question: str
    thread_id: str

class Thema(BaseModel):
    thema: str
    
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
        res = []
        for i in messages.data[0].content[0].text.value.split("\n"):
            if i: 
                if i[0] in '12345':
                    res.append(i)
        return res, thread.id
                
    else:
        return run.status

@app.post("/have_question/")
async def guide(data: Question):
    mission = data.mission
    question = data.question
    thread_id = data.thread_id
    
    message = client.beta.threads.messages.create(
    
    thread_id=thread_id,
    role="user",
    content=f"{mission} {question}"
    )
    
    run = client.beta.threads.runs.create_and_poll(
    thread_id=thread_id,
    assistant_id=assistant_id
    )
    if run.status == 'completed': 
        messages = client.beta.threads.messages.list(
            thread_id=thread_id
        )
        res = []
        for i in messages.data[0].content[0].text.value.split("\n"):
            print(i)
            if i: 
                if i[0] in '12345':
                    res.append(i)
        if not res:
            return i
        else:
            return res
    else:
        return run.status
    
@app.post("/get_teamframe/")
async def create_item(data: Item):
    mbti_types = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
    ]

    mbti_seq = ""
    for m,n in zip(data.mbti, data.num_people):
        mbti_seq += (m+str(n)+' ')
    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=f"{mbti_seq}"
    )
    
    run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id="assistant_key"
    )
    if run.status == 'completed': 
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        res = []
        for i in messages.data[0].content[0].text.value.split("\n"):
            if i:
                tmp = []
                split_arr = i.split()
                # print(split_arr)
                for idx, j in enumerate(split_arr):
                    if j in mbti_types:
                        tmp.append([split_arr[idx],split_arr[idx+1].replace('명','')])
                if tmp:
                    res.append(tmp)
        
            
        return res, i #[[mbti, 명수]], 조합의미
                
    else:
        return run.status
    
    
@app.post("/judge/")
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
        res = []
        for i in messages.data[0].content[0].text.value.split("\n"):
            if i: 
                if i[0] in '12345':
                    res.append(i)
        return res, thread.id
                
    else:
        return run.status
    
    
@app.post("/get_thema/")
async def create_item(data: Thema):
    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=f"{data.thema}를 주로 여행하고싶어"
    )
    
    run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id="assistant_key"
    )
    if run.status == 'completed': 
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        res = []
        flag = -1
        for i in messages.data[0].content[0].text.value.split("\n"):
            if i: 
                if i[0] in '12345':
                    print(i)
                    res.append(i)
                    flag = 2
                    
                elif flag <= 2 and flag >= 0:
                    flag -= 1
                    res.append(i)
                    
        return res[:-1]
                
    else:
        return run.status
