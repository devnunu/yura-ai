from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


class TextProcessor:
    def __init__(self, api_key):
        print(f"api_key:{api_key}")
        self.llm = ChatOpenAI(api_key=api_key, model="gpt-3.5-turbo", temperature=0.7)

        # 시스템 메시지와 사용자 메시지를 위한 프롬프트 템플릿 설정
        self.system_message = (
            """"
                역할설정:
                    - 당신은 핀다라는 핀테크 회사의 UX Writer 입니다.
                    - 주어진 텍스트를 아래의 요구사항과 규칙을 기반으로 새롭게 작성해야합니다.
                요구사항:
                    - 주어진 텍스트는 간결하고 명확하게 작성해야합니다.

                강력한 주의: 위의 조건을 지키지 않는 요약은 무효화됩니다.
            """
        )
        self.prompt_template = """
                주어진 텍스트:
                {text}

                새로운 텍스트:
                """

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_message),
            ("human", self.prompt_template)
        ])

    def rewrite_for_brand(self, input_text):
        formatted_prompt = self.prompt.format(text=input_text)
        output = self.llm.invoke(formatted_prompt).content
        print(f"output:{output}")
        return output
