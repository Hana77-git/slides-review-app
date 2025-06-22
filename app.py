import streamlit as st
import zipfile
import os
import shutil
from PIL import Image
from io import BytesIO
from pathlib import Path
from datetime import datetime

from utils.pptx_reader import extract_text_and_images
from utils.question_generator_gemini import generate_question
from utils.image_search import search_image_sources
from utils.feedback import save_feedback

# タイトル
st.title("🎓 発表スライド評価アシスタント")

# ファイルアップロード
uploaded_file = st.file_uploader("📂 PowerPointスライド（形式）をアップロード", type=["pptx"])

if uploaded_file:
    # 一時ディレクトリ作成
    extract_dir = Path("./temp_slides")
    if extract_dir.exists():
      shutil.rmtree(extract_dir)
    extract_dir.mkdir(parents=True, exist_ok=True)

    # テキストと画像の抽出
    extract_text_and_images(uploaded_file, extract_dir)

    st.header("📊 スライド解析結果")
    slides = sorted(list((extract_dir / "text").glob("*.txt")))
    images = sorted(list((extract_dir / "img").glob("*.png")))


    # --- スライドと質問生成 ---
    all_questions = []
    for i, slide in enumerate(slides):
      with open(slide, "r", encoding="utf-8") as f:
          slide_text = f.read()

      st.subheader(f"Slide {i+1}")
      st.markdown("**📝 スライド内容：**")
      st.text(slide_text)

      st.markdown("**❓ 想定される質問：**")
      question = generate_question(slide_text)
      st.text(question)
      all_questions.append({"slide": i + 1, "text": slide_text, "question": question})

    # --- 質問提案への全体フィードバック ---
    st.markdown("---")
    st.header("🗳 質問提案に対するフィードバック")

    relevance_all = st.slider("質問の関連性（全体評価）", 1, 5)
    helpful_all = st.radio("役に立ったか", ["Good", "Bad"])
    comment_all = st.text_area("自由記述フィードバック")

    if st.button("送信（質問提案フィードバック）"):
        save_feedback({
            "type": "question",
            "relevance": relevance_all,
            "helpful": helpful_all,
            "comment": comment_all,
            "questions": all_questions
        },
        feedback_type="question")
        st.success("質問フィードバックを送信しました ✅")

    # --- 画像と出典推定 ---
    st.markdown("---")
    st.header("🖼 画像と出典推定")

    sources = search_image_sources(images)
    image_feedback_list = []

    for i, image in enumerate(images):
        st.subheader(f"Image {i+1}")
        st.image(image, caption=image, width=300)

        source = sources.get(image)
        st.markdown(f"🔗 出典（推定）：{source}")

        correct = st.radio(f"出典は正確だったか（Image {i+1}）", ["合っていた", "合っていなかった"], key=f"source_feedback_{i}")

        image_feedback_list.append({
            "image_index": i + 1,
            "image_path": str(image),
            "image_source": source,
            "correct": correct
        })

    # --- 画像出典に関するフィードバック送信 ---
    if st.button("送信（画像出典フィードバック）"):
        save_feedback({
            "type": "image_sources",
            "feedback": image_feedback_list
        },
        feedback_type="image_source")
        st.success("画像出典フィードバックを送信しました ✅")



