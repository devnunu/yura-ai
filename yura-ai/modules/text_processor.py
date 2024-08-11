import os
from config.settings import settings
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


class TextProcessor:
    def __init__(self, api_key):
        self.model = ChatOpenAI(openai_api_key=api_key, model="gpt-3.5-turbo", temperature=0, streaming=True)

        self.system_message = (
            """
            당신은 UX Writer 입니다. 
            다음의 텍스트를 아래의 조건에 맞게 재작성하세요.
            {tone}
            """
        )

        self.prompt_template = """
        텍스트:
        {text}

        결과:
        """

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_message),
            ("human", self.prompt_template)
        ])

        self.chain = LLMChain(llm=self.model, prompt=self.prompt)

    def process_text(self, input_text, tone=None):
        tone = tone or settings.default_tone
        response = self.chain.run(text=input_text, tone=tone)
        return response

    def process_text_stream(self, input_text, tone=None):
        tone = tone or settings.default_tone
        output_text = ""

        # 스트리밍된 텍스트 청크를 반복적으로 처리합니다.
        for chunk in self.chain.stream({"text": input_text, "tone": tone}):
            output_text += chunk['text']  # 각 청크의 텍스트를 가져와서 추가합니다.
            yield output_text  # 현재까지의 누적된 텍스트를 반환합니다.


text_processor = TextProcessor(api_key=os.getenv("OPENAI_API_KEY"))
