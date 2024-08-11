from modules.text_processor import text_processor


class UXWriter:
    def __init__(self, brand_name):
        self.brand_name = brand_name

    def rewrite_for_brand(self, input_text):
        tone = f"{self.brand_name}의 브랜드 톤앤 매너"
        return text_processor.process_text(input_text, tone=tone)

    def rewrite_for_brand_stream(self, input_text):
        tone = f"{self.brand_name}의 브랜드 톤앤 매너"
        # process_text_stream에서 나오는 각 청크를 그대로 스트리밍합니다.
        for chunk in text_processor.process_text_stream(input_text, tone=tone):
            yield chunk  # 청크를 바로 반환


ux_writer = UXWriter(brand_name="Finda")
