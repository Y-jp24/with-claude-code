# アイデア管理SaaS - ローカル環境セットアップ

## 必要な環境

- Docker Desktop
- Git
- Node.js 18+ (開発時のみ)
- Python 3.11+ (開発時のみ)

## セットアップ手順

### 1. プロジェクトのクローン

```bash
git clone https://github.com/Y-jp24/with-claude-code.git
cd with-claude-code
```

### 2. 環境変数ファイルの確認

`.env`ファイルが存在することを確認してください。存在しない場合は以下の内容で作成：

```bash
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Google API Configuration
GOOGLE_API_KEY=your_google_api_key_here

# Claude API Configuration
CLAUDE_API_KEY=your_claude_api_key_here
```

### 3. Docker環境での起動

```bash
# ローカル用の設定でDockerコンテナを起動
docker-compose -f docker-compose.local.yml up -d --build

# ログの確認
docker-compose -f docker-compose.local.yml logs -f
```

### 4. アクセス

- **フロントエンド**: http://localhost:3000
- **バックエンドAPI**: http://localhost:8000
- **API仕様書**: http://localhost:8000/docs

### 5. 初期ユーザー作成

ブラウザで http://localhost:3000/register にアクセスして、新しいアカウントを作成してください。

## 開発時のコマンド

### コンテナの管理

```bash
# コンテナの起動
docker-compose -f docker-compose.local.yml up -d

# コンテナの停止
docker-compose -f docker-compose.local.yml down

# コンテナの再起動
docker-compose -f docker-compose.local.yml restart

# ログの確認
docker-compose -f docker-compose.local.yml logs -f

# 特定のサービスのログ確認
docker-compose -f docker-compose.local.yml logs frontend
docker-compose -f docker-compose.local.yml logs backend
```

### データベースの初期化

```bash
# バックエンドコンテナに入る
docker-compose -f docker-compose.local.yml exec backend bash

# データベースファイルの削除（必要な場合）
rm -f /app/idea_management.db

# コンテナを再起動してデータベースを再作成
docker-compose -f docker-compose.local.yml restart backend
```

## トラブルシューティング

### ポートが使用中の場合

```bash
# ポート使用状況の確認
lsof -i :3000
lsof -i :8000

# 使用中のプロセスを停止
kill -9 <PID>
```

### Docker関連の問題

```bash
# Dockerの状態確認
docker ps
docker images

# 古いコンテナ・イメージの削除
docker system prune -a

# 完全リビルド
docker-compose -f docker-compose.local.yml down
docker-compose -f docker-compose.local.yml build --no-cache
docker-compose -f docker-compose.local.yml up -d
```

### フロントエンドの問題

```bash
# Node.jsの依存関係の再インストール
docker-compose -f docker-compose.local.yml exec frontend npm install

# Next.jsキャッシュのクリア
docker-compose -f docker-compose.local.yml exec frontend npm run build
```

## 機能

- ユーザー登録・ログイン
- アイデア管理（作成・編集・削除）
- ダッシュボード（付箋機能）
- 要件定義書の生成（OpenAI/Google/Claude API）

## API仕様

バックエンドが起動している状態で http://localhost:8000/docs にアクセスすると、SwaggerUIでAPI仕様を確認できます。

## 開発環境での直接実行

Dockerを使わずに直接実行する場合：

### バックエンド

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### フロントエンド

```bash
cd frontend
npm install
npm run dev
```
