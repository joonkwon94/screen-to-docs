import os
import time
import uuid
import threading
import keyboard
import pyautogui
from capture import capture_screen, save_image_temp
from gemini_vision import analyze_image_with_gemini, reset_chat_session
from docs_integration import send_to_docs

# 설정: 단축키 지정
NEW_DOC_HOTKEY = 'ctrl+shift+n'
CAPTURE_HOTKEY = 'ctrl+shift+s'
FINISH_HOTKEY = 'ctrl+shift+f'
SET_LOC_HOTKEY = 'ctrl+shift+l'
AUTO_HOTKEY = 'ctrl+shift+a'

TEMP_IMAGE_PATH = 'screenshot_temp.png'
SESSION_ID = str(uuid.uuid4())
next_btn_pos = None
is_auto_running = False

reset_chat_session()

print("==========================================")
print(f" Screen-to-Docs 자동화 프로그램 (Auto-Pilot 탑재) 시작됨 ")
print(f" 📄 새 문서 시작 : '{NEW_DOC_HOTKEY}' (AI 기억 초기화 및 새 문서)")
print(f" 📸 수동 캡처    : '{CAPTURE_HOTKEY}' (현재 화면 캡처)")
print(f" 📍 버튼 위치저장: '{SET_LOC_HOTKEY}' (마우스를 Next 버튼에 올리고 누르세요)")
print(f" 🤖 자동 수면모드: '{AUTO_HOTKEY}' (팝업창에서 장수를 직접 입력하세요)")
print(f" 🏁 기록 종료    : '{FINISH_HOTKEY}' (문서 닫기)")
print("==========================================")

def on_new_doc_pressed():
    global SESSION_ID
    SESSION_ID = str(uuid.uuid4())
    reset_chat_session()
    print(f"\n[{time.strftime('%H:%M:%S')}] 📄 새 문서 모드 전환! 다음 캡처부터는 새로운 구글 문서에 저장됩니다.")

def on_capture_pressed():
    print(f"\n[{time.strftime('%H:%M:%S')}] 📸 화면 캡처 시작...")
    img = capture_screen()
    if not img: return
    save_image_temp(img, TEMP_IMAGE_PATH)
    
    extracted_text = analyze_image_with_gemini(TEMP_IMAGE_PATH)
    if extracted_text and not extracted_text.startswith("[Error]"):
        print("\n--- 추출된 텍스트 요약 ---")
        print(extracted_text)
        print("--------------------------\n")
        send_to_docs(extracted_text, SESSION_ID, action="append")
    else:
        print("[Process] 에러 발생으로 전송 실패.")
    
    if os.path.exists(TEMP_IMAGE_PATH): os.remove(TEMP_IMAGE_PATH)

def on_finish_pressed():
    print(f"\n[{time.strftime('%H:%M:%S')}] 🏁 작업 완료 단축키 감지됨! 문서에 종료 메시지를 기록합니다.")
    send_to_docs("", SESSION_ID, action="finish")

def on_set_location_pressed():
    global next_btn_pos
    next_btn_pos = pyautogui.position()
    print(f"\n[{time.strftime('%H:%M:%S')}] 📍 '우클릭'할 Next 버튼 위치 저장 완료: {next_btn_pos}")
    print("이제 자동 수면모드(Ctrl+Shift+A)를 실행할 수 있습니다.")

def auto_pilot_thread(loop_count):
    global is_auto_running
    is_auto_running = True
    print(f"\n🤖 Auto-Pilot 시작! 총 {loop_count}회 반복합니다.")
    
    for i in range(loop_count):
        if not is_auto_running: break
            
        print(f"\n--- [Auto-Pilot] {i+1}/{loop_count} 번째 페이지 진행 중 ---")
        on_capture_pressed() # 캡처 및 전송
        
        if i < loop_count - 1:
            print(f"  > 캡처 완료. 2초 후 지정된 위치를 '우클릭' 합니다...")
            time.sleep(2)
            
            # 사용자 요청에 따라 '마우스 우클릭' 수행
            pyautogui.rightClick(x=next_btn_pos.x, y=next_btn_pos.y)
            print(f"  > 우클릭 완료. 다음 페이지 로딩을 위해 4초 대기합니다...")
            time.sleep(4) # 화면 로딩 시간 대기
            
    print("\n🤖 Auto-Pilot 모든 반복 종료!")
    on_finish_pressed()
    is_auto_running = False

def on_auto_pilot_pressed():
    global next_btn_pos, is_auto_running
    
    if is_auto_running:
        print("\n[Warning] 이미 자동 모드가 실행 중입니다!")
        return
        
    if next_btn_pos is None:
        print("\n[Error] Next 버튼 위치가 없습니다. 마우스를 버튼에 올리고 Ctrl+Shift+L을 먼저 눌러주세요!")
        return
        
    # 팝업을 띄워 원하는 장수(페이지 수)를 입력받음
    count_str = pyautogui.prompt(text='몇 페이지를 캡처할까요? (숫자만 입력)\n지정된 위치를 "우클릭"하여 다음 페이지로 넘깁니다.', title='수면 모드 설정', default='40')
    
    if count_str and count_str.isdigit():
        count = int(count_str)
        threading.Thread(target=auto_pilot_thread, args=(count,), daemon=True).start()
    else:
        print("\n[Cancel] 입력이 취소되었거나 숫자가 아닙니다.")

keyboard.add_hotkey(NEW_DOC_HOTKEY, on_new_doc_pressed)
keyboard.add_hotkey(CAPTURE_HOTKEY, on_capture_pressed)
keyboard.add_hotkey(FINISH_HOTKEY, on_finish_pressed)
keyboard.add_hotkey(SET_LOC_HOTKEY, on_set_location_pressed)
keyboard.add_hotkey(AUTO_HOTKEY, on_auto_pilot_pressed)

try:
    keyboard.wait('esc')
except KeyboardInterrupt:
    print("프로그램을 종료합니다.")
