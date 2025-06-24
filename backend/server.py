from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from typing import Optional, List

from create_quiz import create_quiz
from load_llm import llm
from prompt_manager import create_chat_system_prompt
from llm_service import generate_quiz_with_llm
from utils import get_artwork_info

app = FastAPI(title="Museum Quiz API", description="美術館クイズAPI", version="1.0.0")

# CORS設定（フロントエンドからのアクセスを許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では具体的なドメインを指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# リクエスト/レスポンスモデル
class QuizRequest(BaseModel):
    json_file_path: Optional[str] = None

class QuizResponse(BaseModel):
    question: str
    artwork_info: str
    session_id: str

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    response: str

# セッション管理（メモリ内で簡易的に実装）
sessions = {}

@app.get("/")
async def root():
    """ヘルスチェック用エンドポイント"""
    return {"message": "Museum Quiz API is running!"}

@app.post("/api/quiz/create", response_model=QuizResponse)
async def create_quiz_endpoint(request: QuizRequest = QuizRequest()):
    """
    新しいクイズを生成するエンドポイント
    """
    try:
        # デフォルトのJSONファイルパス
        json_file_path = request.json_file_path or os.path.join(
            os.path.dirname(__file__), "data", "museum_data_dummy.json"
        )
        
        # クイズ生成
        question, artwork_info = create_quiz(llm, json_file_path)
        
        # セッションID生成（シンプルな実装）
        session_id = f"session_{len(sessions)}"
        
        # チャット用システムプロンプト生成
        system_prompt = create_chat_system_prompt(artwork_info, question)
        
        # セッション保存
        sessions[session_id] = {
            "question": question,
            "artwork_info": artwork_info,
            "system_prompt": system_prompt,
            "messages": [{"role": "system", "content": system_prompt}]
        }
        
        return QuizResponse(
            question=question,
            artwork_info=artwork_info,
            session_id=session_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"クイズ生成に失敗しました: {str(e)}")

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    チャット機能のエンドポイント
    """
    try:
        # セッション確認
        if request.session_id not in sessions:
            raise HTTPException(status_code=404, detail="セッションが見つかりません")
        
        session = sessions[request.session_id]
        
        # ユーザーメッセージを追加
        session["messages"].append({"role": "user", "content": request.message})
        
        # LLMからレスポンス生成
        output = llm.create_chat_completion(session["messages"])
        response_text = output["choices"][0]["message"]["content"]
        
        # アシスタントのレスポンスを追加
        session["messages"].append(output["choices"][0]["message"])
        
        return ChatResponse(response=response_text.strip())
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"チャット処理に失敗しました: {str(e)}")

@app.get("/api/sessions")
async def get_sessions():
    """
    現在のセッション一覧を取得（デバッグ用）
    """
    return {
        "active_sessions": len(sessions),
        "session_ids": list(sessions.keys())
    }

@app.delete("/api/sessions/{session_id}")
async def delete_session(session_id: str):
    """
    指定されたセッションを削除
    """
    if session_id in sessions:
        del sessions[session_id]
        return {"message": f"セッション {session_id} を削除しました"}
    else:
        raise HTTPException(status_code=404, detail="セッションが見つかりません")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
