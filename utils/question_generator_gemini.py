import yaml
import os
import google.generativeai as genai

# config.yaml 読み込み
with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

prompt_template = config["question_prompt_template"]

# APIキー設定（環境変数でもOK）
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# モデル指定（軽量モデル推奨: gemini-1.5-flash）
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_question(slide_text, max_questions=3):
    prompt = prompt_template.format(slide_text=slide_text, max_questions=max_questions)
    response = model.generate_content(prompt)
    return response.text.strip()
