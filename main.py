import os
import time
import uuid
import keyboard
from capture import capture_screen, save_image_temp
from gemini_vision import analyze_image_with_gemini
from docs_integration import send_to_docs

# 설정: 단축키 지정
CAPTURE_HOTKEY = 'ctrl+shift+s'
NEW_DOC_HOTKEY = 'ctrl+shift+n'
TEMP_IMAGE_PATH = 'screenshot_temp.png'

# 이번 실행에 대한 고유 세션 ID 생성
SESSION_ID = str(uuid.uuid4())

print("==========================================")
print(f" Screen-to-Docs 자동화 프로그램 시작됨 ")
print(f" 📸 캡처 단축키: '{CAPTURE_HOTKEY}' (현재 문서에 텍스트 추가)")
print(f" 📄 새 문서 단축키: '{NEW_DOC_HOTKEY}' (새로운 구글 문서 생성)")
print(" 프로그램을 종료하려면 콘솔 창을 닫거나 Ctrl+C를 누르세요.")
print("==========================================")

def on_new_doc_pressed():
    global SESSION_ID
    # 새로운 세션 ID 발급 (다음 캡처부터는 구글 스크립트가 새 문서를 만듭니다)
    SESSION_ID = str(uuid.uuid4())
    print(f"\n[{time.strftime('%H:%M:%S')}] 📄 새 문서 모드 전환! 다음 캡처부터는 완전히 새로운 구글 문서에 저장됩니다.")

def on_capture_pressed():
    print(f"\n[{time.strftime('%H:%M:%S')}] 📸 캡처 단축키 감지됨! 화면 분석 시작.")
    
    # 1. 화면 캡처
    img = capture_screen()
    if not img:
        return
        
    save_image_temp(img, TEMP_IMAGE_PATH)
    
    # 2. Gemini API로 텍스트 추출 및 요약
    extracted_text = analyze_image_with_gemini(TEMP_IMAGE_PATH)
    
    if extracted_text and not extracted_text.startswith("[Error]"):
        print("\n--- 추출된 텍스트 요약 ---")
        print(extracted_text)
        print("--------------------------\n")
        
        # 3. Google Docs로 전송 (세션 ID 포함)
        send_to_docs(extracted_text, SESSION_ID)
    else:
        print("[Process] 추출된 텍스트가 없거나 에러가 발생하여 전송하지 않습니다.")
    
    # 임시 파일 삭제
    if os.path.exists(TEMP_IMAGE_PATH):
        os.remove(TEMP_IMAGE_PATH)
        print(f"[Process] 임시 파일 삭제 완료.")

# 단축키 리스너 등록
keyboard.add_hotkey(NEW_DOC_HOTKEY, on_new_doc_pressed)
keyboard.add_hotkey(CAPTURE_HOTKEY, on_capture_pressed)

# 프로그램이 종료되지 않고 대기하도록 함
try:
    keyboard.wait('esc') # ESC 키를 누르면 종료되도록 대기
except KeyboardInterrupt:
    print("프로그램을 종료합니다.")
