from fastapi import APIRouter

from .endpoints import ideas, users, auth, home, requirements

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["認証"])
api_router.include_router(users.router, prefix="/users", tags=["ユーザー"])
api_router.include_router(ideas.router, prefix="/ideas", tags=["アイデア"])
api_router.include_router(requirements.router, prefix="/requirements", tags=["要件定義"])
api_router.include_router(home.router, prefix="/home", tags=["ホーム"])