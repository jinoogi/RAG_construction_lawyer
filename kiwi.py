import os
from kiwipiepy import Kiwi

def process_text_files(input_dirs, output_dir):
    kiwi = Kiwi()
    
    for input_dir in input_dirs:
        # 입력 폴더의 모든 파일을 순회
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                if file.endswith('.txt'):
                    input_file_path = os.path.join(root, file)
                    
                    # 텍스트 파일 읽기
                    with open(input_file_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                    
                    # 문장으로 나누기
                    sentences = kiwi.split_into_sents(text)
                    
                    # 출력 파일 경로 설정
                    relative_path = os.path.relpath(root, input_dir)
                    output_file_dir = os.path.join(output_dir, relative_path)
                    os.makedirs(output_file_dir, exist_ok=True)
                    output_file_path = os.path.join(output_file_dir, file)
                    
                    # 나뉜 문장을 출력 파일에 저장
                    with open(output_file_path, 'w', encoding='utf-8') as f:
                        for sentence in sentences:
                            f.write(sentence.text + '\n')

# 입력 디렉토리들의 리스트와 출력 디렉토리 경로 설정
input_directories = [
'./kiwi_target'    # 추가적인 입력 디렉토리 경로들을 여기에 추가
]
output_directory = './kiwi_result'

# 함수 실행
process_text_files(input_directories, output_directory)