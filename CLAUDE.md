# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

アイデアから要件定義書を自動生成するSaaSアプリケーション。フロントエンドはNext.js、バックエンドはFastAPIで構築されており、LLM APIを活用してアイデアを要件定義書に変換します。

## 開発コマンド

### バックエンド（FastAPI）
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload          # 開発サーバー起動
python -m pytest                      # テスト実行
```

### フロントエンド（Next.js）
```bash
cd frontend
npm install
npm run dev                           # 開発サーバー起動
npm run build                         # プロダクションビルド
npm run lint                          # ESLint実行
npm run type-check                    # TypeScript型チェック
```

### Docker環境
```bash
docker-compose up --build             # 開発環境起動
docker-compose down                   # 環境停止
```

## アーキテクチャ概要

### ディレクトリ構造
```
idea-management-saas/
├── backend/                          # FastAPIアプリケーション
│   ├── app/
│   │   ├── api/v1/                  # APIエンドポイント
│   │   ├── core/                    # 設定・データベース・セキュリティ
│   │   ├── crud/                    # データベース操作
│   │   ├── models/                  # SQLAlchemyモデル
│   │   ├── schemas/                 # Pydanticスキーマ
│   │   └── services/                # ビジネスロジック（LLM連携など）
│   └── requirements.txt
├── frontend/                         # Next.jsアプリケーション
│   ├── src/
│   │   ├── app/                     # App Router（ページ）
│   │   ├── components/              # 再利用可能コンポーネント
│   │   ├── stores/                  # Zustand状態管理
│   │   └── lib/                     # ユーティリティ
│   └── package.json
├── docker-compose.yml               # 開発環境設定
└── .env                             # 環境変数
```

### 主要機能
1. **認証**: JWT認証（OAuth2 Password Bearer）
2. **アイデア管理**: CRUD操作、コメント、ブックマーク
3. **LLM統合**: OpenAI/Google/Claude APIで要件定義書生成
4. **ホーム画面**: ドラッグ&ドロップ可能な付箋風UI
5. **共有機能**: URLベースでアイデア共有

### データベース
- 開発環境: SQLite
- 本番環境: 環境変数で切り替え可能
- ORM: SQLAlchemy
- マイグレーション: Alembic

## 開発時の注意点

### バックエンド
- APIエンドポイントは`/api/v1/`プレフィックス
- 認証が必要なエンドポイントは`Depends(get_current_active_user)`を使用
- LLM APIキーは環境変数で管理（`.env`ファイル）
- データベースモデル変更時はAlembicマイグレーション作成

### フロントエンド
- 状態管理: Zustand（認証状態など）
- HTTP クライアント: Axios（エラーハンドリング付き）
- スタイリング: Tailwind CSS + カスタムコンポーネント
- アイコン: FontAwesome
- 認証チェック: ページアクセス時の自動リダイレクト

### 環境変数
必須環境変数（`.env`ファイル）:
- `OPENAI_API_KEY`: OpenAI API キー
- `GOOGLE_API_KEY`: Google AI API キー  
- `CLAUDE_API_KEY`: Claude API キー
- `SECRET_KEY`: JWT署名用シークレットキー

## デプロイ
- Railway対応
- Dockerfile: `Dockerfile.backend`、`Dockerfile.frontend`
- 設定ファイル: `railway.json`