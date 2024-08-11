from modules.text_processor import TextProcessor


class UXWriter:
    def __init__(self, brand_name, api_key, callback_handler):
        self.brand_name = brand_name
        self.api_key = api_key
        self.callback_handler = callback_handler
        self.text_processor = TextProcessor(api_key=self.api_key, callback_handler=self.callback_handler)

    def rewrite_for_brand(self, input_text):
        tone = f"{self.brand_name}의 브랜드 톤앤 매너"
        return self.text_processor.process_text(input_text, tone=tone)

    def rewrite_for_brand_stream(self, input_text):
        tone = f"{self.brand_name}의 브랜드 톤앤 매너"
        return self.text_processor.process_text(input_text, tone=tone)

