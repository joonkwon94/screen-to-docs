import os
import time
import keyboard
from capture import capture_screen, save_image_temp
from gemini_vision import analyze_image_with_gemini
from docs_integration import send_to_docs

# 설정: 이 단축키를 누르면 캡처 및 전송이 시작됩니다.
HOTKEY = 'ctrl+shift+s'
TEMP_IMAGE_PATH = 'screenshot_temp.png'

print("==========================================")
print(f" Screen-to-Docs 자동화 프로그램 시작됨 ")
print(f" 단축키 '{HOTKEY}'를 누르면 화면을 캡처합니다.")
print(" 프로그램을 종료하려면 콘솔 창을 닫거나 Ctrl+C를 누르세요.")
print("==========================================")

def on_hotkey_pressed():
    print(f"\n[{time.strftime('%H:%M:%S')}] 단축키 감지됨! 프로세스 시작.")
    
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
        
        # 3. Google Docs로 전송
        send_to_docs(extracted_text)
    else:
        print("[Process] 추출된 텍스트가 없거나 에러가 발생하여 전송하지 않습니다.")
    
    # 임시 파일 삭제
    if os.path.exists(TEMP_IMAGE_PATH):
        os.remove(TEMP_IMAGE_PATH)
        print(f"[Process] 임시 파일({TEMP_IMAGE_PATH}) 삭제 완료.")

# 단축키 리스너 등록
keyboard.add_hotkey(HOTKEY, on_hotkey_pressed)

# 프로그램이 종료되지 않고 대기하도록 함
try:
    keyboard.wait('esc') # ESC 키를 누르면 종료되도록 대기 (백그라운드에서 동작할 땐 이 상태 유지)
except KeyboardInterrupt:
    print("프로그램을 종료합니다.")
