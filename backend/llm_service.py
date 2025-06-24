import json
from load_llm import llm

def generate_quiz_with_llm(system_prompt, instruction_prompt):
    """LLMを使ってクイズを生成する"""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": instruction_prompt}
    ]
    
    output = llm.create_chat_completion(messages)
    response_text = output["choices"][0]["message"]["content"]
    
    try:
        response_json = json.loads(response_text)
        question = response_json.get("question", "クイズの生成に失敗")
        return question, None
    except json.JSONDecodeError:
        print("JSONの解析に失敗")
        print("LLMの出力：")
        print(response_text)
        return "クイズの生成に失敗", "JSON解析エラー"

def chat_with_llm(system_prompt):
    """LLMとのチャット処理を行う"""
    messages = [{"role": "system", "content": system_prompt}]
    
    while True:
        user_input = input("user > ")
        if user_input.lower() in ["exit", "quit", "終了"]:
            print("終了")
            break

        if user_input.strip():
            messages.append({"role": "user", "content": user_input})
            output = llm.create_chat_completion(messages)
            response = output["choices"][0]["message"]["content"]
            print(response.strip(" \n"))
            messages.append(output["choices"][0]["message"])
        else:
            print("質問が空")
