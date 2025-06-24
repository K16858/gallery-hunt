import os
from llama_cpp import Llama

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "sarashina2.2-3b-instruct-v0.1-Q8_0.gguf")

# Llama.cppモデル
llm = Llama(
    model_path=MODEL_PATH,
    temperature=0.7,
    max_tokens=500,
    top_p=0.9,
    n_ctx=4000,
    verbose=False,
)
