import os
from utils import get_artwork_info
import json

def create_quiz(llm, json_file_path):
    """
    クイズを作成する関数
    """
    artwork_info = get_artwork_info(json_file_path)
    
    SYSYTEM_PROMPT = f"""
    あなたは、美術館の案内係です。
    あなたの仕事は，来館者の質問に答えたり，案内をしたりすることです。
    今回、あなたが紹介する絵画の情報は以下の通りです。
    {artwork_info}
    """
    messages = []
    messages.append({"role": "system", "content": SYSYTEM_PROMPT})
    
    INITIAL_PROMPT = """
    あなたは美術館のガイドです。
    来館者が実際に美術館内を巡り、特定の作品を探し出すための「作品発見クイズ」の問題を1問作成してください。
    **問題の要件:**
    * 問題文は、ターゲット作品の「**視覚的な特徴**」「**雰囲気**」「**主なモチーフ**」「**作者や時代の特徴（ヒントとして）**」を組み合わせてください。
    * **作品名や作者名を直接的に明かさないでください**。
    * 来館者がヒントをもとに美術館内を探索し、その作品がどれかを特定できるような内容にしてください。
    * 難易度は**中程度**とし、複数のヒントを組み合わせた文章としてください。
    * 問題文は**日本語**で作成してください。
    * 問題文には、作品のタイトルを含めないでください。
    フォーマットはjson形式で以下のようにすること
    {"thought-of-reasons": "考えた理由", "question": "クイズ"}
    """

    messages.append({"role": "user", "content": INITIAL_PROMPT})
    output = llm.create_chat_completion(messages)
    response_text = output["choices"][0]["message"]["content"]

    try:
        response_json = json.loads(response_text)
        question = response_json.get("question", "クイズの生成に失敗")

        return question, artwork_info
    except json.JSONDecodeError:
        print("JSONの解析に失敗")
        print("LLMの出力：")
        print(response_text)
        return "クイズの生成に失敗", artwork_info
        