import streamlit as st
from config.settings import settings
from modules.ux_writer import ux_writer

st.title("유라 AI - UX Writer Assistant")

st.sidebar.header("설정")
tone = st.sidebar.text_input("텍스트 톤 설정", settings.default_tone)
new_criteria = st.sidebar.text_input("새 텍스트 기준 추가")

if st.sidebar.button("기준 추가"):
    settings.add_criteria(new_criteria)
    st.sidebar.write(f"추가된 기준: {settings.custom_criteria}")

if st.sidebar.button("기준 삭제"):
    settings.remove_criteria(new_criteria)
    st.sidebar.write(f"남은 기준: {settings.custom_criteria}")

input_text = st.text_area("텍스트를 입력하세요:")
if st.button("텍스트 생성"):
    rewritten_text = ux_writer.rewrite_for_brand(input_text)
    st.write("생성된 텍스트:")
    st.write(rewritten_text)