from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from api.database.models import User # 屋台モデル
from pydantic import BaseModel

router = APIRouter()

# Pydanticスキーマ
class UserCreate(BaseModel):
    username: str
    password: str
    email: str 


class UserResponse(BaseModel):
    id: int
    username: str
    password: str
    email: str 

    class Config:
        from_attributes = True  # Pydantic v2 でORM対応

# 作成エンドポイント
@router.post("/users/")
def create_stall(user: UserCreate):
    return JSONResponse({'is_success': User.create(username=user.username, password=user.password, email=user.email)})

# 取得エンドポイント
@router.get("/users/", response_model=List[UserResponse])
def get_stalls():
    try:
        # Userテーブルから全レコードを取得
        users = User.get_list()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
