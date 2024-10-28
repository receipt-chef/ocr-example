import os
import json
import uuid
import time
import requests
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# .env에 api 설정 값, api gateway url 넣으면 됨
CLOVA_API_URL = os.getenv("CLOVA_API_URL")  # 클로바 OCR API URL로 변경
CLOVA_API_KEY = os.getenv("CLOVA_API_KEY")  # 클로바 OCR API Key로 변경

# 폴더 경로 설정
IMAGE_DIR = "images"

def process_receipt_images():
    print("OCR을 시작합니다")
    image_files = [f for f in os.listdir(IMAGE_DIR) if os.path.isfile(os.path.join(IMAGE_DIR, f))]
    if not image_files:
        print(f"{IMAGE_DIR} 폴더에 이미지를 넣어주십쇼")
        return

    for image_file in image_files:
        image_path = os.path.join(IMAGE_DIR, image_file)

        # Clova OCR API 요청
        with open(image_path, 'rb') as img_file:
            headers = {"X-OCR-SECRET": CLOVA_API_KEY}
            files = {"file": img_file}
            data = {
                "version": "V2",
                "requestId": str(uuid.uuid4()),
                "timestamp": int(time.time() * 1000),
                "lang": "ko",
                "images": [{"format": "jpg", "name": image_file}]
            }
            response = requests.post(CLOVA_API_URL, headers=headers, files=files, data={"message": json.dumps(data)})
        
        print(f"서버에 {image_file} 요청 했습니다")

        if response.status_code == 200:
            ocr_data = response.json()
            display_text_data(ocr_data, image_file)
            print(f"{image_file} 처리 성공")
        else:
            print(f"에러 발생 {image_file}: 상태코드 {response.status_code}, 상태문구 {response.text}")
    
    print("완료")

def display_text_data(ocr_data, image_file):
    try:
        # 이미지의 텍스트 필드를 콘솔에 출력
        text_data = ocr_data['images'][0]['fields']
        print(f"{image_file} OCR 결과:")
        for field in text_data:
            print(field['inferText'])
        print("\n" + "="*40 + "\n")  # 출력 구분선
    except (KeyError, IndexError):
        print(f"{image_file}에서 텍스트를 찾을 수 없습니다.")
