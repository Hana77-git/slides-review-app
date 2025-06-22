import yaml
import os
import time
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

# config.yaml 読み込み
with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

prompt_template = config["question_prompt_template"]

# APIキー設定（環境変数でもOK）
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# モデル指定（軽量モデル推奨: gemini-1.5-flash）
model = genai.GenerativeModel("gemini-1.5-flash")


def generate_question(slide_text, max_questions=3, max_retries=3, wait_seconds=45):
    """
    スライドテキストから質問を生成する関数。
    Gemini APIのレート制限（429）に対して自動リトライを行う。

    Parameters:
    - slide_text (str): スライドの内容
    - max_questions (int): 質問数
    - max_retries (int): 最大リトライ回数
    - wait_seconds (int): レート制限時の待機秒数

    Returns:
    - str: 質問テキスト
    """
    prompt = prompt_template.format(slide_text=slide_text, max_questions=max_questions)

    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except ResourceExhausted as e:
            if attempt < max_retries - 1:
                print(f"[Warning] レート制限に達しました。{wait_seconds}秒後に再試行します... ({attempt+1}/{max_retries})")
                time.sleep(wait_seconds)
            else:
                print("[Error] レート制限によりリクエストが失敗しました。最大リトライ回数を超えました。")
                raise
