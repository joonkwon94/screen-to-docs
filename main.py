import os
import time
import uuid
import keyboard
from capture import capture_screen, save_image_temp
from gemini_vision import analyze_image_with_gemini, reset_chat_session
from docs_integration import send_to_docs

# 설정: 단축키 지정
NEW_DOC_HOTKEY = 'ctrl+shift+n'
CAPTURE_HOTKEY = 'ctrl+shift+s'
FINISH_HOTKEY = 'ctrl+shift+f'
TEMP_IMAGE_PATH = 'screenshot_temp.png'

# 이번 실행에 대한 고유 세션 ID 생성 및 AI 기억 초기화
SESSION_ID = str(uuid.uuid4())
reset_chat_session()

print("==========================================")
print(f" Screen-to-Docs 자동화 프로그램 시작됨 ")
print(f" 📄 새 문서 단축키: '{NEW_DOC_HOTKEY}' (새 구글 문서 준비)")
print(f" 📸 캡처 단축키  : '{CAPTURE_HOTKEY}' (현재 문서에 내용 추가)")
print(f" 🏁 종료 단축키  : '{FINISH_HOTKEY}' (현재 문서 기록 완료 및 닫기)")
print(" 프로그램을 종료하려면 콘솔 창을 닫거나 Ctrl+C를 누르세요.")
print("==========================================")

def on_new_doc_pressed():
    global SESSION_ID
    SESSION_ID = str(uuid.uuid4())
    reset_chat_session()
    print(f"\n[{time.strftime('%H:%M:%S')}] 📄 새 문서 모드 전환! 다음 캡처부터는 새로운 구글 문서에 저장됩니다.")

def on_capture_pressed():
    print(f"\n[{time.strftime('%H:%M:%S')}] 📸 캡처 단축키 감지됨! 화면 분석 시작.")
    
    img = capture_screen()
    if not img:
        return
        
    save_image_temp(img, TEMP_IMAGE_PATH)
    
    extracted_text = analyze_image_with_gemini(TEMP_IMAGE_PATH)
    
    if extracted_text and not extracted_text.startswith("[Error]"):
        print("\n--- 추출된 텍스트 요약 ---")
        print(extracted_text)
        print("--------------------------\n")
        
        send_to_docs(extracted_text, SESSION_ID, action="append")
    else:
        print("[Process] 추출된 텍스트가 없거나 에러가 발생하여 전송하지 않습니다.")
    
    if os.path.exists(TEMP_IMAGE_PATH):
        os.remove(TEMP_IMAGE_PATH)
        print(f"[Process] 임시 파일 삭제 완료.")

def on_finish_pressed():
    print(f"\n[{time.strftime('%H:%M:%S')}] 🏁 작업 완료 단축키 감지됨! 문서에 종료 메시지를 기록합니다.")
    send_to_docs("", SESSION_ID, action="finish")

# 단축키 리스너 등록
keyboard.add_hotkey(NEW_DOC_HOTKEY, on_new_doc_pressed)
keyboard.add_hotkey(CAPTURE_HOTKEY, on_capture_pressed)
keyboard.add_hotkey(FINISH_HOTKEY, on_finish_pressed)

# 프로그램이 종료되지 않고 대기하도록 함
try:
    keyboard.wait('esc')
except KeyboardInterrupt:
    print("프로그램을 종료합니다.")
