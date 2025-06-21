import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def search_image_sources(image_paths):
    results = {}
    for path in image_paths:
        try:
            image = Image.open(path)
            response = model.generate_content(["この画像の出典を推定してください。", image])
            results[path] = response.text
        except Exception as e:
            results[path] = f"検索失敗: {e}"
    return results
