# 開発チーム向けガイド

## 新しい開発者の参加手順

### 1. 初回セットアップ

```bash
# 1. リポジトリをクローン
git clone <repository-url>
cd with-claude-code

# 2. 自動セットアップスクリプトを実行
./setup-dev.sh

# 3. Dockerで起動
docker-compose up
```

### 2. 環境変数の設定

#### 必須の環境変数

開発に必要な環境変数は自動で生成されますが、LLM機能を使う場合は以下を設定：

```bash
# backend/.env
OPENAI_API_KEY=your_key_here    # OpenAI GPT使用時
GOOGLE_API_KEY=your_key_here    # Google Gemini使用時  
CLAUDE_API_KEY=your_key_here    # Claude使用時
```

### 3. データベース管理

#### 初期化

```bash
cd backend
python init_db.py
```

#### マイグレーション（将来対応予定）

```bash
# Alembicを使用
alembic upgrade head
```

#### 開発用データのリセット

```bash
# データベースを削除して再作成
rm backend/idea_management.db
python backend/init_db.py
```

## よくある問題と解決方法

### ❌ "frontend/src/lib/axios.ts が見つからない"

**原因**: 過去に `.gitignore` で `lib/` が除外されていたため

**解決方法**: 
```bash
git pull  # 最新の状態を取得（現在は修正済み）
```

### ❌ "Module not found: @/lib/axios"

**原因**: パスエイリアスの設定問題

**解決方法**: 
相対パス import に変更済み（修正不要）

### ❌ データベースファイルがない

**原因**: `.gitignore` でデータベースファイルが除外されている（正常）

**解決方法**:
```bash
python backend/init_db.py
```

### ❌ CORS エラー

**原因**: フロントエンドとバックエンドのURL設定が正しくない

**解決方法**:
1. `frontend/.env.local` で `NEXT_PUBLIC_API_URL` を確認
2. `backend/.env` で `BACKEND_CORS_ORIGINS` を確認

## ファイル構成の説明

### 追跡されるファイル
- アプリケーションコード（`/frontend/src/`, `/backend/app/`）
- 設定ファイル（`docker-compose.yml`, `package.json` など）
- ドキュメント（`README.md`, この文書など）
- 初期化スクリプト（`init_db.py`, `setup-dev.sh`）

### 追跡されないファイル（.gitignore）
- データベースファイル（`*.db`, `*.sqlite`）
- 環境変数ファイル（`.env`, `.env.local`）
- 依存関係（`node_modules/`, `__pycache__/`）
- IDE設定（`.vscode/`, `.idea/`）

## Git ワークフロー

### ブランチ戦略

```bash
main        # 本番環境用
develop     # 開発環境用  
feature/*   # 機能開発用
hotfix/*    # 緊急修正用
```

### コミット規約

```bash
feat: 新機能追加
fix: バグ修正
docs: ドキュメント更新
style: コードスタイル修正
refactor: リファクタリング
test: テスト追加・修正
chore: その他の作業
```

## テスト

### バックエンドテスト

```bash
cd backend
pytest
```

### フロントエンドテスト

```bash
cd frontend
npm test
```

## デプロイ

### Railway へのデプロイ

Railway に自動デプロイされます。
- `main` ブランチ → 本番環境
- `develop` ブランチ → ステージング環境

## トラブルシューティング

### ログの確認

```bash
# すべてのサービスのログ
docker-compose logs

# 特定のサービスのログ
docker-compose logs frontend
docker-compose logs backend
```

### コンテナの再構築

```bash
# キャッシュを使わずに再構築
docker-compose build --no-cache
```

### 完全リセット

```bash
# すべてのコンテナとボリュームを削除
docker-compose down -v
docker system prune -a
```

## 開発のヒント

### ホットリロード

- フロントエンド: ファイル変更時に自動リロード
- バックエンド: `--reload` オプションで自動リロード

### API テスト

FastAPI の自動生成ドキュメントを活用:
http://localhost:8000/docs

### デバッグ

1. VS Code の Dev Containers 拡張機能を使用
2. `docker-compose.yml` でデバッグポートを公開
3. ブレークポイントを設定してデバッグ
