from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage


class TextProcessor:
    def __init__(self, api_key, callback_handler):
        self.api_key = api_key
        self.callback_handler = callback_handler
        self.system_message_template = """
            당신은 UX Writer 입니다.
            다음의 텍스트를 아래의 조건에 맞게 재작성하세요.
            {tone}
        """
        self.prompt_template = """
            텍스트:
            {text}

            결과:
        """

        self.llm = ChatOpenAI(
            openai_api_key=self.api_key,
            model="gpt-3.5-turbo",
            temperature=0,
            streaming=True,
            callbacks=[self.callback_handler],
        )

    def process_text(self, input_text, tone=None):
        system_message = SystemMessage(content=self.system_message_template.format(tone=tone))
        human_message = HumanMessage(content=self.prompt_template.format(text=input_text))
        messages = [system_message, human_message]

        response = self.llm(messages)
        return response
