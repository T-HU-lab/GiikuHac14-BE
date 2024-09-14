from fastapi import APIRouter, Depends, HTTPException, Request, Header, Body
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from api.database.models import Review, User # 屋台モデル
from pydantic import BaseModel, Field
from api.routers.auth import get_current_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Pydanticスキーマ
# Reviewスキーマ（レビュー）
# レビューモデルの定義
class ReviewBase(BaseModel):
    stall_id: int
    rating: int = Field(..., ge=1, le=5)  # 1〜5の範囲でバリデーション
    comment: str

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True 
        from_attributes=True# ORMとの互換性を有効にする

# レビューの作成エンドポイント
@router.post("/reviews/", response_model=ReviewResponse)
def create_review(review: ReviewCreate, current_user: User = Depends(get_current_user)):
    try:
        # レビューをデータベースに保存
        new_review = Review.create(
            stall_id=review.stall_id,
            user_id=current_user.id,
            rating=review.rating,
            comment=review.comment
        )
        return ReviewResponse.from_orm(new_review) # FastAPIが自動的にresponse_modelの形式でレスポンスを返す
    except Exception as e:
        # エラーハンドリング
        raise HTTPException(status_code=500, detail=str(e))

# レビューリスト取得エンドポイント
@router.get("/reviews/", response_model=List[ReviewResponse])
def get_reviews():
    try:
        # Stallテーブルから全レコードを取得
        reviews = Review.get_list()
        return reviews
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 店idからレビューリスト取得エンドポイント
@router.get("/reviews/{stall_id}", response_model=List[ReviewResponse])
def get_reviews_by_stall_id(stall_id: int):
    try:
        
        reviews = Review.get_by_stall_id(stall_id)
        return reviews
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ユーザーidからレビューリスト取得エンドポイント
@router.get("/reviews/{user_id}", response_model=List[ReviewResponse])
def get_reviews_by_user_id(user_id: int):
    try:
        
        reviews = Review.get_list_by_user_id(user_id)
        return reviews
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
