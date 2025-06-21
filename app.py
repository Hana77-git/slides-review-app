import streamlit as st
import zipfile
import os
import shutil
from PIL import Image
from io import BytesIO
from pathlib import Path

from utils.pptx_reader import extract_text_and_images
from utils.question_generator_gemini import generate_question
from utils.image_search import search_image_sources

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

    for i, slide in enumerate(slides):
      with open(slide, "r", encoding="utf-8") as f:
        slide_text = f.read()
      
      st.subheader(f"Slide {i+1}")
      st.markdown("** スライド内容：**")
      st.text(slide_text)

      st.markdown("**❓ 想定される質問：**")
      question = generate_question(slide_text)
      st.text(question)
      
    for i, image in enumerate(images):
      st.subheader(f"Image {i+1}")
      st.image(image, caption=image, width=300)
    
    sources = search_image_sources(images)
    for key, value in sources.items():
      st.write(f"**{key}**:")
      st.write(f" 🔗 出典（推定）{value}")
