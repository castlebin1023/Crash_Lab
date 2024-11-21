from fastapi import APIRouter
import sys
import os
import state_manager
response = None
question = None
# 현재 파일의 상위 경로를 sys.path에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# 이제 상위 경로에 있는 모듈을 임포트할 수 있습니다.
"""import gptchat as gpt
gpt.gpt_response = None
gpt.question = None
"""
router = APIRouter()

@router.post("/gptOutput")
def get_gptOutput():
    return {"gptresponse": state_manager.response}

@router.post("/UserInput")
def get_UserInput():
    return {"usermessage": state_manager.question}
