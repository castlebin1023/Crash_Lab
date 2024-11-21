from fastapi import FastAPI
from routers import task
import uvicorn
import gptchat as gpt
import asyncio
import state_manager  # 상태 관리 모듈 임포트
from fastapi.middleware.cors import CORSMiddleware

gpt.gpt_response = None
gpt.question = None
task.response = None
task.question = None
app = FastAPI()
app.include_router(task.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.on_event("startup")
async def startup_event():
    # 서버 시작 시 비동기적으로 주기적 실행 설정
    asyncio.create_task(run_text_message_periodically())
async def run_text_message_periodically():
    while True:
        gpt.textMessage()  # gpt.textMessage()가 주기적으로 실행
        task.response = gpt.gpt_response
        task.question = gpt.question
        state_manager.question, state_manager.response = [gpt.gpt_response, gpt.question]
        print(state_manager.question)
        

        await asyncio.sleep(10)  # 10초마다 실행 (필요에 따라 조정)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
 