# GitHub Codespacesのポート転送とネットワークの仕組み

## 概要
GitHub Codespacesは、クラウド上で動作する開発環境であり、ローカルマシンから遠隔でアクセスします。このため、Codespacesで起動したアプリケーションのポートには特別な仕組みが必要です。

## ポート転送の基本構造

### 1. Codespacesの内部ネットワーク
```
┌─────────────────────────────────────┐
│         Codespace Environment      │
│  ┌─────────────┐  ┌─────────────┐  │
│  │  Frontend   │  │   Backend   │  │
│  │ Port: 3000  │  │ Port: 8000  │  │
│  └─────────────┘  └─────────────┘  │
│         │                 │         │
│    localhost:3000   localhost:8000  │
└─────────────────────────────────────┘
```

### 2. GitHub Codespacesのプロキシシステム
```
User Browser
    ↓
GitHub Proxy Server (*.app.github.dev)
    ↓
Port Forwarding Service
    ↓
Codespace Container
    ↓
Application (localhost:8000)
```

## ポート可視性の違い

### Private (デフォルト)
- Codespacesの所有者のみアクセス可能
- GitHub認証が必要
- URL: `https://codespace-name-port.app.github.dev`
- 認証フローが必要なため、API呼び出しで問題が発生

### Public
- インターネット上の誰でもアクセス可能
- GitHub認証不要
- 同じURL: `https://codespace-name-port.app.github.dev`
- 直接アクセス可能、API呼び出しが正常動作

## 今回の問題と解決

### 問題の流れ
1. フロントエンド(Port 3000): Publicに自動設定済み ✅
2. バックエンド(Port 8000): Privateのまま ❌
3. フロントエンドからバックエンドAPIへの呼び出し: 認証エラー

### 解決手順
1. VS Codeのポートタブでポート8000を確認
2. 右クリック → "ポートの可視性" → "Public"に変更
3. バックエンドAPIが外部からアクセス可能に

## セキュリティ考慮事項

### Public設定のリスク
- APIエンドポイントが外部に公開される
- 適切な認証・認可が重要
- 本番環境では絶対に避けるべき

### 開発環境での対策
- JWT認証の実装 ✅ (今回実装済み)
- テスト用データのみ使用
- 定期的なCredential変更

## ネットワークフローの詳細

### ログイン前
```
Browser → Frontend(Public) → Login API
         ↓
Browser ← JWT Token ← Login API
```

### ログイン後のAPI呼び出し
```
Browser → Frontend(Public) → API Call with JWT
         ↓
Backend(Public) → Verify JWT → Response
         ↓
Browser ← Response ← Frontend
```

## 代替手段

### 1. Dockerコンテナ間通信の利用
```yaml
# docker-compose.yml
environment:
  - NEXT_PUBLIC_API_URL=http://backend:8000/api/v1
```

### 2. GitHub CLIでのポート転送
```bash
gh codespace ports forward 8000:8000 --codespace $CODESPACE_NAME
```

### 3. VSCodeのポート転送コマンド
```bash
code --tunnel --accept-server-license-terms
```

## まとめ
GitHub Codespacesのポート公開は、クラウド開発環境での重要な機能です。適切に設定することで、ローカル開発と同様の体験を実現できますが、セキュリティ面での注意が必要です。
