import pdfplumber

def pdf_to_txt(document):
    with pdfplumber.open(f"{document}.pdf") as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""  # None 처리
        
    with open(f"{document}.txt", "w", encoding="utf-8") as txt_file:
        txt_file.write(text)

pdf_to_txt("중처법")