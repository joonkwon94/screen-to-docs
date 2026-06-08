import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
    print("WARNING: GEMINI_API_KEY가 설정되지 않았습니다. .env 파일을 확인해 주세요.")

client = genai.Client(api_key=GEMINI_API_KEY)

current_chat = None

def reset_chat_session():
    """
    Gemini의 이전 대화 기록을 완전히 초기화하고 새로운 챗 세션을 엽니다.
    """
    global current_chat
    if not client.api_key:
        return

    system_instruction = """
당신은 토플(TOEFL) 문제 추출 어시스턴트입니다.
사용자는 토플 시험 화면을 계속해서 캡처하여 보낼 것입니다. 화면에는 일반적으로 긴 '지문(Passage)'과 그에 딸린 '문제(Question) 및 보기'가 포함되어 있습니다.

[중요 규칙]
1. 지문과 문제를 명확히 구분하여 마크다운 서식으로 추출하세요.
2. 이전 캡처본과 비교하여 동일한 지문이 반복될 경우, 지문 텍스트는 전부 생략하고 "*(지문 동일함)*" 이라고만 적은 뒤, 새롭게 등장한 '문제와 보기'만 추출하세요.
3. 불필요한 UI(타이머, 버튼, 프로그램 틀 등)는 철저히 무시하세요.
"""
    print("[Gemini] AI의 기억(챗 세션)을 초기화합니다. 이제부터 새로운 지문을 인식합니다.")
    current_chat = client.chats.create(
        model='gemini-2.5-flash',
        config=types.GenerateContentConfig(
            system_instruction=system_instruction
        )
    )

def analyze_image_with_gemini(image_path):
    """
    캡처된 이미지를 기억을 유지하는 Gemini Chat 세션으로 전송하여 텍스트를 추출합니다.
    """
    global current_chat
    if not client.api_key:
        return "[Error] API Key가 등록되지 않았습니다."

    if current_chat is None:
        reset_chat_session()

    print(f"[Gemini] 토플 문제 분석 중... ({image_path})")
    
    prompt = "이 화면에서 텍스트를 추출해 줘. 만약 지문이 이전 화면과 같다면 지문은 빼고 새로운 문제만 줘."

    try:
        from PIL import Image
        img = Image.open(image_path)
        
        response = current_chat.send_message([prompt, img])
        
        print("[Gemini] 분석 완료!")
        return response.text
        
    except Exception as e:
        print(f"[Gemini Error] 분석 중 오류 발생: {e}")
        return f"분석 중 오류 발생: {e}"
