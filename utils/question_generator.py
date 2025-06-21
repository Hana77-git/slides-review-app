import yaml
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline


with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

prompt_template = config["question_prompt_template"]

# 初期化（必要に応じてキャッシュ活用）
model_id = "google/gemma-2b-it"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto")

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

def generate_question(slide_text, max_questions=3):
    prompt = prompt_template.format(slide_text=slide_text, max_questions=max_questions)
    output = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.7)
    return output[0]['generated_text'].replace(prompt, "").strip()
