#!/bin/bash

# 開発環境セットアップスクリプト
# 新しい開発者がプロジェクトをクローンした後に実行するスクリプト

set -e  # エラーが発生したら停止

echo "🚀 開発環境のセットアップを開始します..."

# 1. 必要なディレクトリを作成
echo "📁 必要なディレクトリを作成中..."
mkdir -p backend/data
mkdir -p frontend/src/lib

# 2. 環境変数ファイルの作成
echo "⚙️  環境変数ファイルを作成中..."

# バックエンド用 .env ファイル
if [ ! -f "backend/.env" ]; then
    cat > backend/.env << EOF
# Database
DATABASE_URL=sqlite:///./idea_management.db

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000","http://localhost:8000"]

# LLM APIs (オプション - 使用する場合は設定してください)
OPENAI_API_KEY=
GOOGLE_API_KEY=
CLAUDE_API_KEY=
EOF
    echo "✅ backend/.env を作成しました"
else
    echo "ℹ️  backend/.env は既に存在します"
fi

# フロントエンド用 .env.local ファイル
if [ ! -f "frontend/.env.local" ]; then
    cat > frontend/.env.local << EOF
# API URL
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
EOF
    echo "✅ frontend/.env.local を作成しました"
else
    echo "ℹ️  frontend/.env.local は既に存在します"
fi

# 3. データベースの初期化
echo "🗄️  データベースを初期化中..."
cd backend
if [ -f "idea_management.db" ]; then
    echo "⚠️  既存のデータベースが見つかりました。バックアップを作成します..."
    cp idea_management.db "idea_management.db.backup.$(date +%Y%m%d_%H%M%S)"
fi

python init_db.py
cd ..

# 4. 依存関係のインストール（Docker以外の場合）
if command -v python3 &> /dev/null && command -v npm &> /dev/null; then
    echo "📦 依存関係をインストール中..."
    
    # Python依存関係
    echo "  - Python依存関係..."
    cd backend
    pip install -r requirements.txt
    cd ..
    
    # Node.js依存関係
    echo "  - Node.js依存関係..."
    cd frontend
    npm install
    cd ..
else
    echo "ℹ️  Python3またはnpmが見つかりません。Dockerを使用してください。"
fi

echo ""
echo "🎉 セットアップが完了しました！"
echo ""
echo "次のステップ:"
echo "1. Docker使用の場合:"
echo "   docker-compose up"
echo ""
echo "2. ローカル開発の場合:"
echo "   # バックエンド (ターミナル1)"
echo "   cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "   # フロントエンド (ターミナル2)"
echo "   cd frontend && npm run dev"
echo ""
echo "アクセス先:"
echo "- フロントエンド: http://localhost:3000"
echo "- バックエンドAPI: http://localhost:8000"
echo "- API文書: http://localhost:8000/docs"
echo ""
echo "初期ユーザー:"
echo "- admin@example.com (パスワード: admin123)"
echo "- demo@example.com (パスワード: demo123)"
