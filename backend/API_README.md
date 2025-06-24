# Museum Quiz API

美術館クイズシステムのFastAPI実装

## 起動方法

### 1. 依存関係のインストール
```bash
pip install fastapi uvicorn python-multipart
```

### 2. サーバー起動

#### 方法1: バッチファイルを使用（Windows）
```bash
start_server.bat
```

#### 方法2: コマンドラインから直接起動
```bash
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

#### 方法3: Pythonから直接起動
```bash
python server.py
```

## API エンドポイント

### ベースURL
```
http://localhost:8000
```

### エンドポイント一覧

#### 1. ヘルスチェック
- **GET** `/`
- サーバーの動作確認

#### 2. クイズ生成
- **POST** `/api/quiz/create`
- 新しいクイズとセッションを生成
- レスポンス: `question`, `artwork_info`, `session_id`

#### 3. チャット
- **POST** `/api/chat`
- セッションIDとメッセージを送信してLLMと対話
- リクエスト: `session_id`, `message`
- レスポンス: `response`

#### 4. セッション管理
- **GET** `/api/sessions` - アクティブなセッション一覧を取得
- **DELETE** `/api/sessions/{session_id}` - 指定セッションを削除

## API ドキュメント

サーバー起動後、以下のURLでSwagger UIでAPIドキュメントを確認できます：
```
http://localhost:8000/docs
```

## 使用例

### 1. クイズ生成
```javascript
fetch('http://localhost:8000/api/quiz/create', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({})
})
.then(response => response.json())
.then(data => {
  console.log('クイズ:', data.question);
  console.log('セッションID:', data.session_id);
});
```

### 2. チャット
```javascript
fetch('http://localhost:8000/api/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    session_id: 'session_0',
    message: 'モナリザ'
  })
})
.then(response => response.json())
.then(data => {
  console.log('AI応答:', data.response);
});
```

## 技術仕様

- **フレームワーク**: FastAPI
- **LLM**: llama.cpp (sarashina2.2-3b-instruct)
- **CORS**: すべてのオリジンからのアクセスを許可（開発環境用）
- **セッション管理**: メモリ内ストレージ（本番環境では永続化ストレージを推奨）

## 注意事項

- 現在のセッション管理はメモリ内で行っているため、サーバー再起動でセッションが失われます
- 本番環境では、CORS設定を適切なドメインに制限してください
- LLMの初期化に時間がかかる場合があります
