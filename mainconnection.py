"""
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

import crash_lang as cr
import time
import threading
import openai
import os
from openai import OpenAI
@app.route('/api/chat',methods=['POST'])

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
"""
from flask import Flask, request, jsonify
from flask_cors import CORS

import crash_lang as cr
import openai
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI()

# 초기 대화 기록 설정
conversation_history = [{"role": "system", "content": "Hello! How can I help you today?"}]

# 사용자로부터 질문을 받는 엔드포인트
@app.route('/api/chat', methods=['POST'])
def chat():
    micindex = request.json.get('micindex', 0)  # POST 요청에서 micindex를 가져옴

    # 음성 인식을 통해 질문을 얻음
    question = cr.google_free(micindex)
    if question is None:
        return jsonify({'error': 'Voice not recognized or API error'}), 400

    # 사용자의 질문을 대화 기록에 추가
    conversation_history.append({"role": "user", "content": question})
    
    # GPT-3.5-turbo 모델을 사용해 응답을 생성
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation_history
        )
        answer = completion.choices[0].message.content

        # 생성된 응답을 대화 기록에 추가
        conversation_history.append({"role": "assistant", "content": answer})
        
        # 응답을 반환
        return jsonify({'response': answer})
    except Exception as e:
        print(f"Can't access API; {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
