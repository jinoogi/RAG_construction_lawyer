import fitz  # PyMuPDF

def extract_text_with_overlapping_graphics(pdf_path, tolerance=1):
    """
    그래픽 요소와 겹치는 텍스트를 추출합니다.
    
    Args:
        pdf_path (str): PDF 파일 경로.
        tolerance (float): 텍스트와 그래픽의 bbox가 겹치는 것으로 간주할 허용 오차.
    
    Returns:
        list: 그래픽 요소와 겹치는 텍스트 정보 리스트.
    """
    doc = fitz.open(pdf_path)
    overlapping_texts = []

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        
        # 그래픽 요소 위치 추출
        graphics = []
        for obj in page.get_drawings():
            graphics.append({
                "type": obj["type"],
                "bbox": obj["rect"],
                "page_num": page_num + 1
            })

        # 텍스트 추출 및 그래픽 요소와 비교
        for block in page.get_text("dict")["blocks"]:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text_bbox = span["bbox"]
                        text = span["text"]
                        font_size = span["size"]
                        font_name = span["font"]

                        # 그래픽 요소와 겹치는지 확인
                        is_overlapping = False
                        for graphic in graphics:
                            graphic_bbox = graphic["bbox"]

                            # 텍스트와 그래픽의 bbox가 겹치는지 확인
                            if (text_bbox[0] < graphic_bbox[2] + tolerance and text_bbox[2] > graphic_bbox[0] - tolerance and
                                text_bbox[1] < graphic_bbox[3] + tolerance and text_bbox[3] > graphic_bbox[1] - tolerance):
                                is_overlapping = True
                                break
                        
                        # 겹치는 텍스트만 저장
                        if is_overlapping:
                            overlapping_texts.append({
                                "text": text,
                                "font_size": font_size,
                                "font_name": font_name,
                                "text_bbox": text_bbox,
                                "graphic_bbox": graphic_bbox,
                                "page_num": page_num + 1
                            })

    return overlapping_texts

# 사용 예시
pdf_path = "중처법.pdf"
overlapping_texts = extract_text_with_overlapping_graphics(pdf_path)

# 결과 출력
for item in overlapping_texts:
    print(f"Text: {item['text']}, Font Size: {item['font_size']}, Font: {item['font_name']}, Text Position: {item['text_bbox']}, Page: {item['page_num']}")
    print(f"Overlapping Graphic Position: {item['graphic_bbox']}")
