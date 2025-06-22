import os
import json
from datetime import datetime

def save_feedback(data, feedback_type, save_dir="feedback_logs"):
    os.makedirs(save_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{feedback_type}_{timestamp}.json"
    path = os.path.join(save_dir, filename)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return path
