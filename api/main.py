from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import stall, user, review, item, auth

app = FastAPI()

# CORSの設定を追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://10.31.1.65:3000"],  # フロントエンドのURL（ローカルホストの場合）
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可
    allow_headers=["*"],  # すべてのHTTPヘッダーを許可
)

app.include_router(stall.router)
app.include_router(user.router)
app.include_router(review.router)
app.include_router(item.router)
app.include_router(auth.router)
