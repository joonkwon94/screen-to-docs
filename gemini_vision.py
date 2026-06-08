import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Gemini API 초기화
# .env 파일에서 GEMINI_API_KEY를 자동으로 읽어옵니다.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
    print("WARNING: GEMINI_API_KEY가 설정되지 않았습니다. .env 파일을 확인해 주세요.")

client = genai.Client(api_key=GEMINI_API_KEY)

def analyze_image_with_gemini(image_path):
    """
    캡처된 이미지를 Gemini Vision API로 전송하여 텍스트를 추출하고 요약합니다.
    """
    if not client.api_key:
        return "[Error] API Key가 등록되지 않았습니다."

    print(f"[Gemini] 이미지 분석 중... ({image_path})")
    
    prompt = """
    이 이미지는 사용자의 컴퓨터 화면을 캡처한 것입니다.
    이미지 안에 있는 주요 텍스트 내용들을 읽어내고, 불필요한 UI 요소(메뉴바 등)는 무시해 주세요.
    추출한 텍스트를 논리적인 구조와 깔끔한 마크다운 서식으로 정리해서 반환해 주세요.
    """

    try:
        # PIL 이미지를 파일로 업로드하거나 직접 넘길 수 있습니다.
        # 최신 google-genai SDK에서는 이미지를 직접 다루는 방법이 모델마다 다를 수 있으므로
        # 가장 안정적인 파일 경로 기반으로 처리하거나 File API를 활용합니다.
        
        # 임시로 genai.types.File 업로드 방식 사용 (또는 base64)
        # 최신 SDK는 PIL Image 객체를 직접 지원하기도 합니다.
        from PIL import Image
        img = Image.open(image_path)
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[prompt, img]
        )
        
        print("[Gemini] 분석 완료!")
        return response.text
        
    except Exception as e:
        print(f"[Gemini Error] 분석 중 오류 발생: {e}")
        return f"분석 중 오류 발생: {e}"
