import crash_lang as cr
import time
import threading
import openai
import os
from openai import OpenAI

# 환경 변수에서 API 키 가져오기
openai.api_key = os.getenv("OPENAI_API_KEY")  # 환경 변수 설정 확인
if openai.api_key is None:
    print("API 키를 설정해주세요.")
    exit()
def ask_gpt(prompt):
    try:
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt},
        ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Can't access API;{e}")
        return None
    
micindex = 6 
client = OpenAI()

question = cr.google_free(micindex)
gpt_response = ask_gpt(question)
print("GPT Answer:", gpt_response)
cr.speak(gpt_response,"ko")
