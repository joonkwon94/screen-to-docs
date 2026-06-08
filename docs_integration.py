import os
import requests
from dotenv import load_dotenv

load_dotenv()

APPS_SCRIPT_URL = os.getenv("GOOGLE_APPS_SCRIPT_URL")

def send_to_docs(text_content, session_id):
    """
    추출된 텍스트를 Google Apps Script Web App URL로 전송합니다.
    """
    if not APPS_SCRIPT_URL or APPS_SCRIPT_URL == "your_google_apps_script_url_here":
        print("[Docs Error] GOOGLE_APPS_SCRIPT_URL이 설정되지 않았습니다. .env 파일을 확인해 주세요.")
        return False

    print("[Docs] Google Docs로 전송 중...")
    
    payload = {
        "text": text_content,
        "session_id": session_id
    }
    
    try:
        response = requests.post(APPS_SCRIPT_URL, json=payload)
        
        if response.status_code == 200:
            print("[Docs] 성공적으로 문서에 추가되었습니다!")
            return True
        else:
            print(f"[Docs Error] 전송 실패: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"[Docs Error] 전송 중 오류 발생: {e}")
        return False
