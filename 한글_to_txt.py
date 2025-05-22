import os
import re
import subprocess

def get_english_numbers(filename):
    return ''.join(re.findall(r'[A-Za-z0-9]', filename))

def convert_hwp_to_txt(hwp_path, txt_path):
    # hwp5txt 명령어를 올바르게 호출합니다.
    subprocess.run(['hwp5txt', '--output', txt_path, hwp_path])

def main(input_folder):
    for filename in os.listdir(input_folder):
        if filename.endswith('.hwp'):
            hwp_path = os.path.join(input_folder, filename)
            base_name = os.path.splitext(filename)[0]
            txt_name = base_name + '.txt'
            txt_path = os.path.join(".", txt_name)
            convert_hwp_to_txt(hwp_path, txt_path)
            print(f"Converted {hwp_path} to {txt_path}")

if __name__ == "__main__":
    folders = ["."]
    for input_folder in folders:
        main(input_folder)