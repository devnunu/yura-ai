import streamlit as st
from dotenv import load_dotenv
import os
from config.settings import settings
from modules.ux_writer import UXWriter
from langchain.callbacks.base import BaseCallbackHandler

# 환경 변수 로드
load_dotenv()


# 세션 상태에 메시지를 저장하는 함수
def save_message(message, role):
    st.session_state.messages.append({"role": role, "content": message})


# 대화창에 메시지를 출력하는 함수
def send_message(message, role, save=True):
    with st.chat_message(role):
        st.markdown(message)
    if save:
        save_message(message, role)


# 대화 기록을 화면에 출력하는 함수
def paint_history():
    for message in st.session_state.messages:
        send_message(message["content"], message["role"], save=False)


# CallbackHandler 클래스 정의
class ChatCallbackHandler(BaseCallbackHandler):
    def __init__(self):
        super().__init__()
        self.message = ""
        self.message_box = None

    def on_llm_start(self, *args, **kwargs):
        self.message = ""
        self.message_box = st.empty()  # 빈 컨테이너 생성

    def on_llm_new_token(self, token, *args, **kwargs):
        self.message += token
        # 빈 컨테이너를 업데이트하여 최신 메시지 표시
        if self.message_box:
            self.message_box.markdown(self.message)

    def on_llm_end(self, *args, **kwargs):
        save_message(self.message, "ai")


# 페이지 설정
st.set_page_config(layout="wide")
st.title("유라 AI - UX Writer Assistant")

# 사이드바에 메뉴 버튼 생성
st.sidebar.title("메뉴")
if "menu" not in st.session_state:
    st.session_state.menu = "대화하기"

# 사이드바 버튼들
if st.sidebar.button("대화하기"):
    st.session_state.menu = "대화하기"

if st.sidebar.button("설정"):
    st.session_state.menu = "설정"

# "대화하기" 메뉴 선택 시
if st.session_state.menu == "대화하기":
    st.header("유라와 대화하세요")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 대화 기록 표시
    paint_history()

    # API 키 및 CallbackHandler 생성
    api_key = os.getenv("OPENAI_API_KEY")
    callback_handler = ChatCallbackHandler()

    # UXWriter 인스턴스 생성
    ux_writer = UXWriter(brand_name="Finda", api_key=api_key, callback_handler=callback_handler)

    # 사용자 입력 필드 및 전송 버튼을 chat_input으로 처리
    user_input = st.chat_input("텍스트를 입력하세요:")

    if user_input:
        # 사용자 메시지 추가
        send_message(user_input, "user")

        # AI의 응답을 st.chat_message("ai")로 스트리밍
        with st.chat_message("ai"):
            callback_handler.message_box = st.empty()  # 빈 컨테이너 초기화
            ux_writer.rewrite_for_brand_stream(user_input)

# "설정" 메뉴 선택 시
elif st.session_state.menu == "설정":
    st.header("설정")

    new_criteria_col1, new_criteria_col2 = st.columns([3, 1])

    with new_criteria_col1:
        new_criteria = st.text_input("새 텍스트 기준 추가", label_visibility="collapsed")

    with new_criteria_col2:
        if st.button("추가"):
            if new_criteria:
                settings.add_criteria(new_criteria)
                new_criteria = ""

    st.subheader("현재 추가된 조건 리스트")

    if settings.custom_criteria:
        for criterion in settings.custom_criteria:
            item_col1, item_col2 = st.columns([4, 1])

            with item_col1:
                st.text_input(label="", value=criterion, disabled=True, label_visibility="collapsed")

            with item_col2:
                if st.button("X", key=criterion):
                    settings.remove_criteria(criterion)
    else:
        st.write("추가된 조건이 없습니다.")
