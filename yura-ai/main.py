import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from config import OPENAI_API_KEY
from modules.text_processor import TextProcessor

app = Flask(__name__)
CORS(app)

# TextProcessor 초기화
text_processor = TextProcessor(api_key=OPENAI_API_KEY)

# 기본 라우트 설정
@app.route('/')
def index():
    return "Welcome to Yura AI - UX Writer Assistant!"

@app.route('/process', methods=['POST'])
def process_text():
    data = request.json
    user_input = data.get('text')

    # 텍스트 처리
    processed_text = text_processor.rewrite_for_brand(user_input)

    return jsonify({'processed_text': processed_text})


if __name__ == '__main__':
    app.run(debug=True)
