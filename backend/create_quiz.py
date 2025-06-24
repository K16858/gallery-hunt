from utils import get_artwork_info
from prompt_manager import create_quiz_generation_prompt, create_quiz_instruction
from llm_service import generate_quiz_with_llm

def create_quiz(llm, json_file_path):
    """
    クイズを作成する関数
    """
    artwork_info = get_artwork_info(json_file_path)
    system_prompt = create_quiz_generation_prompt(artwork_info)
    instruction_prompt = create_quiz_instruction()
    
    question, error = generate_quiz_with_llm(system_prompt, instruction_prompt)
    
    if error:
        print(f"エラー: {error}")
    
    return question, artwork_info
