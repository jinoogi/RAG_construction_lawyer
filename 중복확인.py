import fitz  # PyMuPDF

def detect_duplicate_text(pdf_path, tolerance=1):
    doc = fitz.open(pdf_path)
    duplicates = []

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        seen_texts = []  # 각 텍스트의 위치와 내용을 저장할 리스트

        for block in page.get_text("dict")["blocks"]:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text_bbox = span["bbox"]
                        text = span["text"]
                        
                        # 중복 텍스트 확인
                        is_duplicate = any(
                            (abs(text_bbox[0] - t["bbox"][0]) < tolerance and 
                             abs(text_bbox[1] - t["bbox"][1]) < tolerance and 
                             text == t["text"])
                            for t in seen_texts
                        )
                        
                        if is_duplicate:
                            duplicates.append({
                                "text": text,
                                "bbox": text_bbox,
                                "page_num": page_num + 1
                            })
                        else:
                            seen_texts.append({"text": text, "bbox": text_bbox})

    return duplicates

pdf_path = "중처법.pdf"
duplicate_texts = detect_duplicate_text(pdf_path)

# 중복된 텍스트 출력
for item in duplicate_texts:
    print(f"Duplicate Text: {item['text']}, Position: {item['bbox']}, Page: {item['page_num']}")
