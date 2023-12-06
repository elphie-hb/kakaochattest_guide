#-*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi import BackgroundTasks
from fastapi.responses import HTMLResponse
from dto import ChatbotRequest
from samples import simple_text_sample, basic_card_sample, commerce_card_sample
from callback import callback_handler
import openai

openai.api_key = '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'
SYSTEM_MSG = "당신은 카카오 서비스 제공자입니다."
app = FastAPI()

@app.get("/")
async def home():
    page = """
    <html>
        <body>
            <h2>카카오 챗봇빌더 스킬 예제입니다 ^^14</h2>
        </body>
    </html>
    """
    return HTMLResponse(content=page, status_code=200)

@app.post("/skill/hello")
def skill(req: ChatbotRequest):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_MSG},
            {"role": "user", "content": req.userRequest.utterance},
        ],
        temperature=0,
    )
    output_text = response.choices[0].message.content
    simple_text_sample2 = {
        "version": "2.0",
        "useCallback" : true,
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": output_text
                    }
                }
            ]
        }
    }
    return simple_text_sample2

@app.post("/skill/basic-card")
async def skill(req: ChatbotRequest):
    return basic_card_sample

@app.post("/skill/commerce-card")
async def skill(req: ChatbotRequest):
    return commerce_card_sample

@app.post("/callback")
async def skill(req: ChatbotRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(callback_handler, req)
    out = {
        "version" : "2.0",
        "useCallback" : True,
        "data": {
            "text" : "생각하고 있는 중이에요😘 \n15초 정도 소요될 거 같아요 기다려 주실래요?!"
        }
    }
    return out
