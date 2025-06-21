import os
import google.generativeai as genai
import yaml
from PIL import Image

with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

prompt_template = config["image_source_prompt_template"]

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def search_image_sources(image_paths):
    results = {}
    for path in image_paths:
        try:
            image = Image.open(path)
            response = model.generate_content([prompt_template, image])
            results[path] = response.text
        except Exception as e:
            results[path] = f"検索失敗: {e}"
    return results
