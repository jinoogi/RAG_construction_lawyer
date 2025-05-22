import fitz  # PyMuPDF

def extract_bold_like_text_by_font(pdf_path):
    doc = fitz.open(pdf_path)
    extracted_data = []

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        for block in page.get_text("dict")["blocks"]:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"]
                        font_size = span["size"]  # 글씨 크기
                        bbox = span["bbox"]
                        font_name = span["font"]  # 글꼴 이름 추출
                        
                        # 글꼴 이름에 'Bold', 'Black', 'Heavy'가 포함된 경우 볼드체로 간주
                        is_bold_like = any(keyword in font_name.lower() for keyword in ["bold", "black", "heavy"])

                        extracted_data.append({
                            "text": text,
                            "font_size": font_size,
                            "font_name": font_name,
                            "bbox": bbox,
                            "is_bold_like": is_bold_like,
                            "page_num": page_num + 1
                        })

    return extracted_data

# PDF 경로 설정
pdf_path = "중처법.pdf"
data = extract_bold_like_text_by_font(pdf_path)

# 볼드체로 추정되는 텍스트 출력
for item in data:
    print(item)
