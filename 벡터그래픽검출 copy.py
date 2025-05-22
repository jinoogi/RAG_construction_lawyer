import fitz  # PyMuPDF

def extract_bold_like_text_by_graphic_overlap(pdf_path):
    doc = fitz.open(pdf_path)
    bold_like_texts = []

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        
        # 페이지의 텍스트와 그래픽 요소를 각각 저장
        text_spans = []
        graphics = []

        # 텍스트 추출
        for block in page.get_text("dict")["blocks"]:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text_spans.append({
                            "text": span["text"],
                            "font_size": span["size"],
                            "font_name": span["font"],
                            "bbox": span["bbox"],
                            "page_num": page_num + 1
                        })

        # 그래픽 요소 추출
        for obj in page.get_drawings():
            graphics.append({
                "type": obj["type"],
                "bbox": obj["rect"],
                "page_num": page_num + 1
            })
        
        # 텍스트와 그래픽 요소 위치 비교
        for text in text_spans:
            text_bbox = text["bbox"]
            
            # 텍스트와 그래픽 요소의 bbox가 겹치는지 확인
            for graphic in graphics:
                graphic_bbox = graphic["bbox"]
                
                # 겹치는 경우를 확인 (텍스트와 그래픽의 bbox가 일부라도 겹치면 볼드체로 추정)
                if (text_bbox[0] < graphic_bbox[2] and text_bbox[2] > graphic_bbox[0] and
                    text_bbox[1] < graphic_bbox[3] and text_bbox[3] > graphic_bbox[1]):
                    
                    bold_like_texts.append({
                        "text": text["text"],
                        "font_size": text["font_size"],
                        "font_name": text["font_name"],
                        "bbox": text_bbox,
                        "page_num": page_num + 1,
                        "graphic_type": graphic["type"],
                        "graphic_bbox": graphic_bbox
                    })
                    break  # 그래픽 요소 하나와 겹치면 추가 후 다음 텍스트로 이동

    return bold_like_texts

# 사용 예시
pdf_path = "중처법.pdf"
bold_like_texts = extract_bold_like_text_by_graphic_overlap(pdf_path)

# 볼드체로 추정되는 텍스트 출력
for item in bold_like_texts:
    print(f"Text: {item['text']}, Font Size: {item['font_size']}, Font: {item['font_name']}, Position: {item['bbox']}, Page: {item['page_num']}")
    print(f"Overlapping Graphic Type: {item['graphic_type']}, Graphic Position: {item['graphic_bbox']}")
