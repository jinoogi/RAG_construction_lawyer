from striprtf.striprtf import rtf_to_text

# 원본 RTF 파일 경로와 출력할 텍스트 파일 경로 설정
input_file_path = "중대재해 처벌 등에 관한 법률(법률)(제17907호)(20220127).doc"
output_file_path = "중대재해_처벌_등에_관한_법률.txt"

# 바이너리 모드로 파일을 열고 수동으로 디코딩
with open(input_file_path, "rb") as file:
    rtf_content = file.read().decode("latin1", errors="ignore")  # 문제가 되는 바이트 무시

# 텍스트로 변환
text = rtf_to_text(rtf_content)

# 변환된 텍스트를 텍스트 파일로 저장
with open(output_file_path, "w", encoding="utf-8") as output_file:
    output_file.write(text)

print(f"텍스트가 {output_file_path}에 저장되었습니다.")
