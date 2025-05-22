import fitz  # PyMuPDF

def check_graphic_elements(pdf_path):
    doc = fitz.open(pdf_path)
    graphics_info = []

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        
        # 페이지의 모든 그래픽 요소 확인
        for obj in page.get_drawings():
            graphics_info.append({
                "type": obj["type"],
                "bbox": obj["rect"],
                "page_num": page_num + 1
            })

    return graphics_info

pdf_path = "중처법.pdf"
graphics = check_graphic_elements(pdf_path)

# 그래픽 요소 출력
for item in graphics:
    print(f"Graphic Type: {item['type']}, Position: {item['bbox']}, Page: {item['page_num']}")
