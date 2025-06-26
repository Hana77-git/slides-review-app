import sys
from pathlib import Path
import shutil
import difflib

sys.path.append(str(Path(__file__).resolve().parent.parent / "utils"))

from pptx_reader import extract_text_and_images
from image_search import search_image_sources

# テスト用ファイルパス
test_pptx = Path("./test/data/test_image_source.pptx")
answer_txt = Path("./test/data/test_image_source_answer.txt")

# 一時的に画像やテキストを保存するディレクトリ
extract_dir = Path("./temp_slides")
if extract_dir.exists():
    shutil.rmtree(extract_dir)
extract_dir.mkdir(parents=True, exist_ok=True)

# 正解読み込み
def load_answers(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

# 類似度を計算
def similarity(a, b):
    return difflib.SequenceMatcher(None, a.strip(), b.strip()).ratio()

# 出力と正解を比較し、評価を出す
def evaluate(predictions, correct_answers, threshold=0.95):
    total = len(correct_answers)
    correct = 0
    mismatches = []

    for i, (pred, correct_answer) in enumerate(zip(predictions, correct_answers)):
        sim = similarity(pred, correct_answer)
        if sim >= threshold:
            correct += 1
        else:
            mismatches.append((i + 1, pred, correct_answer, sim))

    accuracy = correct / total * 100
    return accuracy, mismatches

# スライドから画像とテキストを抽出（前処理）
extract_text_and_images(test_pptx, extract_dir)

# 正解読み込み
answers = load_answers(answer_txt)

# 画像ファイルを取得しソースを推論
images = sorted(list((extract_dir / "img").glob("*.png")))
sources = search_image_sources(images)

# 評価実行
accuracy, mismatches = evaluate(sources, answers)

print(f"正答率（閾値95%）: {accuracy:.2f}%")

if mismatches:
    print("\n❌ 不一致の出力:")
    for idx, pred, correct, sim in mismatches:
        print(f"\n--- {idx} --- 類似度: {sim:.3f}")
        print(f"予測: {pred}")
        print(f"正解: {correct}")
