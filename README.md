# アイデア管理SaaS

アイデアから要件定義書を自動生成し、Git管理できるSaaSアプリケーション。

## 機能

- 📝 アイデアの作成・編集・削除
- 🤖 LLM（OpenAI/Google/Claude）を使った要件定義書の自動生成
- 💬 アイデアへのコメント機能
- 🔖 ブックマーク機能
- 🔗 共有機能（編集可能/閲覧のみ）
- 🏠 カスタマイズ可能なホーム画面（付箋風UI）

## 技術スタック

- **フロントエンド**: Next.js 14, TypeScript, Tailwind CSS
- **バックエンド**: FastAPI, Python 3.11
- **データベース**: SQLite（本番環境では変更可能）
- **デプロイ**: Railway, Docker

## 開発環境のセットアップ

### 前提条件

- Docker と Docker Compose がインストールされていること
- Node.js 18+ (ローカル開発の場合)
- Python 3.11+ (ローカル開発の場合)

### 環境変数の設定

`.env`ファイルに以下の環境変数を設定してください：

```env
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key

# Google API Configuration
GOOGLE_API_KEY=your_google_api_key

# Claude API Configuration
CLAUDE_API_KEY=your_claude_api_key

# App Secret Key
SECRET_KEY=your_secret_key_here
```

### Docker を使った起動

```bash
# コンテナをビルドして起動
docker-compose up --build

# バックグラウンドで起動
docker-compose up -d
```

アプリケーションは以下のURLでアクセスできます：
- フロントエンド: http://localhost:3000
- バックエンドAPI: http://localhost:8000
- API ドキュメント: http://localhost:8000/docs

### ローカル開発

#### バックエンド

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### フロントエンド

```bash
cd frontend
npm install
npm run dev
```

## デプロイ

### Railway へのデプロイ

1. Railway アカウントを作成: https://railway.app/
2. 新しいプロジェクトを作成
3. GitHub リポジトリと連携
4. 環境変数を設定:
   ```
   OPENAI_API_KEY=your_openai_api_key
   GOOGLE_API_KEY=your_google_api_key
   CLAUDE_API_KEY=your_claude_api_key
   SECRET_KEY=your_secret_key_here
   DATABASE_URL=sqlite:///./idea_management.db
   ENVIRONMENT=production
   ```
5. デプロイ（自動的にDockerfileを使用してビルド）

### デプロイ後の設定

- Railway提供のURLでAPIにアクセス可能
- フロントエンドは別途Vercel等にデプロイ推奨
- 本番環境では適切なCORS設定とセキュリティ設定を追加

## ライセンス

MIT