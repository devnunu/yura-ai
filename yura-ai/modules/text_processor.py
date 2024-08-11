import os
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from config.settings import settings

API_KEY = os.getenv("OPENAI_API_KEY")

class TextProcessor:
    def __init__(self, api_key):
        self.api_key = api_key
        self.model = ChatOpenAI(api_key=api_key, model="gpt-3.5-turbo", temperature=0)
        self.prompt_template = ChatPromptTemplate.from_template(
            "다음 텍스트를 '{tone}' 톤으로 재작성하세요:\n\n{input_text}"
        )
        self.chain = LLMChain(llm=self.model, prompt=self.prompt_template)

    def process_text(self, input_text, tone=None):
        tone = tone or settings.default_tone
        response = self.chain.run(input_text=input_text, tone=tone)
        return response

text_processor = TextProcessor(api_key=API_KEY)
