import os
from PIL import ImageGrab

def capture_screen():
    """
    현재 화면 전체를 캡처하여 PIL Image 객체로 반환합니다.
    """
    try:
        print("[Capture] 화면 캡처 중...")
        image = ImageGrab.grab()
        return image
    except Exception as e:
        print(f"[Capture Error] 캡처 중 오류 발생: {e}")
        return None

def save_image_temp(image, temp_path="temp_screenshot.png"):
    """
    캡처한 이미지를 임시 파일로 저장합니다.
    """
    try:
        image.save(temp_path)
        print(f"[Capture] 이미지가 {temp_path} 에 저장되었습니다.")
        return temp_path
    except Exception as e:
        print(f"[Capture Error] 이미지 저장 중 오류 발생: {e}")
        return None
