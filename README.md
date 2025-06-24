# Gallery-Hunt

美術館での作品探索を楽しくするインタラクティブなクイズシステムです。LLMを活用して、来館者が美術作品を発見する体験を提供します。

## 概要

Gallery-Huntは、美術館来館者が作品を探索しながら楽しめるクイズアプリケーションです。AIガイドが作品の特徴を元にしたクイズを出題し、来館者はヒントを頼りに館内で実際の作品を見つけ出します。

## 機能

- **AIクイズ生成**: 作品情報を基にした探索型クイズの自動生成
- **インタラクティブチャット**: リアルタイムでのヒント提供と回答確認
- **美術館ガイド体験**: 作品名や作者名を明かさない段階的なヒントシステム
- **レスポンシブUI**: モダンなReact.js + TypeScriptフロントエンド

## システム構成

```
Gallery-Hunt/
├── backend/           # Python FastAPI バックエンド
│   ├── data/         # 美術作品データ
│   ├── model/        # LLMモデルファイル
│   └── *.py          # API、プロンプト管理、LLMサービス
├── gallery-hunt/     # React.js フロントエンド
│   ├── src/          # TypeScriptソースコード
│   └── public/       # 静的ファイル
└── docs/             # プロジェクト仕様書
```

## 技術スタック

### バックエンド
- **Python 3.11+**
- **FastAPI** - RESTful API
- **LLM (ローカルモデル)** - sarashina2.2-3b-instruct

### フロントエンド
- **React.js 18+**
- **TypeScript**
- **Vite** - ビルドツール
- **ESLint** - コード品質管理

## セットアップ

### 前提条件
- Python 3.11以上
- Node.js 18以上
- Git

### 1. リポジトリのクローン
```bash
git clone <repository-url>
cd museum-llm
```

### 2. バックエンドのセットアップ
```powershell
cd backend

# 仮想環境の作成と有効化
python -m venv venv
.\venv\Scripts\Activate.ps1

# 依存関係のインストール
pip install fastapi uvicorn python-multipart llama-cpp-python

# サーバー起動
python main.py
# または
.\start_server.bat
```

### 3. フロントエンドのセットアップ
```powershell
cd gallery-hunt

# 依存関係のインストール
npm install

# 開発サーバー起動
npm run dev
```

## 使用方法

1. **バックエンドサーバー起動**: `http://localhost:8000`でAPIサーバーが起動
2. **フロントエンド起動**: `http://localhost:5173`でWebアプリが起動
3. **クイズ開始**: 作品選択後、AIガイドとの対話を開始
4. **作品探索**: ヒントを頼りに美術館内で実際の作品を発見

## API仕様

詳細なAPI仕様は [`backend/API_README.md`](backend/API_README.md) を参照してください。

主要エンドポイント:
- `POST /generate-quiz` - クイズ生成
- `POST /chat` - チャット対話
- `GET /artworks` - 作品一覧取得

## データ構造

美術作品データは `backend/data/museum_data_dummy.json` で管理されています。

```json
{
  "id": "M001",
  "title": "作品名",
  "artist": "作者名",
  "era": "時代",
  "genre": "ジャンル",
  "year": 制作年,
  "location": "展示場所",
  "keywords": ["キーワード配列"],
  "description": "作品説明",
  "hint_easy": "簡単ヒント",
  "hint_medium": "中程度ヒント", 
  "hint_hard": "難しいヒント"
}
```

## 開発

### プロジェクト仕様
詳細な仕様は [`docs/specification.md`](docs/specification.md) を参照してください。

---
