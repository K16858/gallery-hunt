from create_quiz import create_quiz
from load_llm import llm
from prompt_manager import create_chat_system_prompt
from llm_service import chat_with_llm

def main():
    JSON_FILE_PATH = "data/museum_data_dummy.json"
    question, artwork_info = create_quiz(llm, JSON_FILE_PATH)
    system_prompt = create_chat_system_prompt(artwork_info, question)
    chat_with_llm(system_prompt)

if __name__ == "__main__":
    main()