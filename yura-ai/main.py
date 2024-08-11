import streamlit as st
from config.settings import settings
from modules.ux_writer import ux_writer


# 메시지를 전송하고 대화창을 업데이트하는 함수
def send_message():
    user_input = st.session_state["user_input"]
    if user_input:
        # 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": user_input})

        # 유라의 응답 생성
        response = ux_writer.rewrite_for_brand(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})

        # 입력 필드를 초기화합니다.
        st.session_state["user_input"] = ""


st.set_page_config(layout="wide")
st.title("유라 AI - UX Writer Assistant")

left_column, right_column = st.columns([1, 2])

# 좌측: 조건 리스트와 조건 추가/삭제 기능
with left_column:
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

# 우측: 유라와의 대화창
with right_column:
    st.header("유라와 대화하세요")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 대화 메시지 표시
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.markdown(message["content"])
        else:
            with st.chat_message("assistant"):
                st.markdown(message["content"])

    input_col1, input_col2 = st.columns([8, 1])

    with input_col1:
        st.text_input("텍스트를 입력하세요:", key="user_input", label_visibility="collapsed", on_change=send_message)

    with input_col2:
        st.button("전송", on_click=send_message)
