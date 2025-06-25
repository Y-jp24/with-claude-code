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

## 🚀 クイックスタート

### 1. プロジェクトのクローン

```bash
git clone <repository-url>
cd with-claude-code
```

### 2. 自動セットアップ（推奨）

```bash
# 開発環境を自動でセットアップ
./setup-dev.sh
```

このスクリプトが以下を自動で行います：
- 必要なディレクトリの作成
- 環境変数ファイルの生成
- データベースの初期化
- 初期ユーザーの作成

### 3. Docker で起動

```bash
docker-compose up
```

### 4. アクセス

- **フロントエンド**: http://localhost:3000
- **バックエンドAPI**: http://localhost:8000
- **API文書**: http://localhost:8000/docs

### 5. ログイン

初期ユーザー：
- **admin@example.com** (パスワード: admin123)
- **demo@example.com** (パスワード: demo123)

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

### デプロイ方法

#### バックエンド（Railway）

1. Railway アカウントを作成: https://railway.app/
2. 新しいプロジェクトを作成
3. GitHub リポジトリと連携: `Y-jp24/with-claude-code`
4. 環境変数を設定:
   ```
   OPENAI_API_KEY=your_openai_api_key
   GOOGLE_API_KEY=your_google_api_key
   CLAUDE_API_KEY=your_claude_api_key
   SECRET_KEY=your_secret_key_here
   DATABASE_URL=sqlite:///./idea_management.db
   ENVIRONMENT=production
   ```
5. デプロイ（`railway.json`と`Dockerfile.production`を使用）

#### フロントエンド（推奨: Vercel）

1. Vercel アカウントを作成: https://vercel.com/
2. GitHub リポジトリと連携
3. **Root Directory**: `frontend` を設定
4. 環境変数を設定:
   ```
   NEXT_PUBLIC_API_URL=https://your-railway-backend-url.railway.app/api/v1
   ```
5. デプロイ

#### フロントエンド（Railway）

1. Railway プロジェクトで **New Service** → **GitHub Repo**
2. 同じGitHubリポジトリ `Y-jp24/with-claude-code` を選択
3. サービス名を「frontend」に変更
4. **Settings** → **Source** → **Root Directory** を `frontend` に設定
5. 環境変数を設定:
   ```
   NEXT_PUBLIC_API_URL=https://your-railway-backend-url.railway.app/api/v1
   NODE_ENV=production
   ```
6. デプロイ完了

**注意**: Railwayでは各サービスが個別の`railway.json`を使用します。
- バックエンド: ルートの`railway.json` + `Dockerfile.production`
- フロントエンド: `frontend/railway.json` + Nixpacks

### デプロイ後の設定

- **バックエンド**: Railway提供のURLでAPIにアクセス可能
- **フロントエンド**: Vercel or Railway提供のURLでアクセス可能
- **CORS設定**: 本番環境では適切なオリジンを設定推奨

## ライセンス

MIT