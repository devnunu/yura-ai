from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from config import SLACK_BOT_TOKEN, SLACK_APP_TOKEN, SLACK_SIGNING_SECRET, OPENAI_API_KEY
from modules.text_processor import TextProcessor

# 슬랙봇 초기화
app = App(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)

# TextProcessor 초기화
text_processor = TextProcessor(api_key=OPENAI_API_KEY)


# 슬랙봇에 메시지가 도착했을 때 처리하는 이벤트 핸들러
@app.message("")
def handle_message_events(message, say):
    say(f"요청하신 텍스트를 처리해볼게요! 잠시만 기다려주세요 :smile:")
    # 텍스트 처리
    user_input = message['text']
    processed_text = text_processor.rewrite_for_brand(user_input)
    say(f"\n{processed_text}")


# 슬랙앱 실행
if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
