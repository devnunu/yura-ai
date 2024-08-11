from modules.text_processor import text_processor

class UXWriter:
    def __init__(self, brand_name):
        self.brand_name = brand_name

    def rewrite_for_brand(self, input_text):
        tone = f"{self.brand_name}의 브랜드 톤앤 매너"
        return text_processor.process_text(input_text, tone=tone)

ux_writer = UXWriter(brand_name="Finda")
