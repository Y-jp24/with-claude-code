#!/usr/bin/env python3
"""
データベース初期化スクリプト
新しい開発環境でデータベースを作成し、初期データを投入します。
"""

import sys
import os
from pathlib import Path

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.core.database import engine, Base
from app.models import user, idea, home  # すべてのモデルをインポート
from app.core.security import get_password_hash
from sqlalchemy.orm import sessionmaker

def create_database():
    """データベースとテーブルを作成"""
    print("データベースとテーブルを作成中...")
    Base.metadata.create_all(bind=engine)
    print("✅ データベースとテーブルを作成しました")

def create_initial_data():
    """初期データを作成"""
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        # 既存のユーザーがいるかチェック
        from app.crud.crud_user import user as user_crud
        existing_user = user_crud.get_by_email(db, email="admin@example.com")
        
        if not existing_user:
            print("初期ユーザーを作成中...")
            # 管理者ユーザーを作成
            admin_user = user_crud.create(db, obj_in={
                "email": "admin@example.com",
                "name": "管理者",
                "hashed_password": get_password_hash("admin123")
            })
            
            # デモユーザーを作成
            demo_user = user_crud.create(db, obj_in={
                "email": "demo@example.com", 
                "name": "デモユーザー",
                "hashed_password": get_password_hash("demo123")
            })
            
            print("✅ 初期ユーザーを作成しました")
            print("  - admin@example.com (パスワード: admin123)")
            print("  - demo@example.com (パスワード: demo123)")
        else:
            print("ℹ️  初期ユーザーは既に存在します")
            
    except Exception as e:
        print(f"❌ 初期データ作成エラー: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """メイン処理"""
    print("🚀 データベース初期化を開始します...")
    
    try:
        create_database()
        create_initial_data()
        print("🎉 データベース初期化が完了しました！")
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
