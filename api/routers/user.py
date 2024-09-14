from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from api.database.models import User # 屋台モデル
from pydantic import BaseModel
from api.routers.auth import get_current_user
router = APIRouter()

# Pydanticスキーマ
class UserCreate(BaseModel):
    username: str
    password: str
    email: str 


class UserResponse(BaseModel):
    id: int
    username: str
    email: str 

    class Config:
        from_attributes = True  # Pydantic v2 でORM対応

# 作成エンドポイント
@router.post("/users/")
def create_stall(user: UserCreate):
    return JSONResponse({'is_success': User.create(username=user.username, password=user.password, email=user.email)})

# 取得エンドポイント
@router.get("/users/", response_model=UserResponse)
def get_user_by_token(user: User=Depends(get_current_user)):
    return user
