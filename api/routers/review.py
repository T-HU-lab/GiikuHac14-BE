from fastapi import APIRouter, Depends, HTTPException, Request, Header, Body
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from api.database.models import Review, User, Stall # 屋台モデル
from api.routers.stall import StallResponse, StallBase
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

class Reviewranking(BaseModel):
    ranking: List[StallResponse]

    class Config:
        orm_mode = True 
        from_attributes = True  # ORMとの互換性を有効にする


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
## /reviews/{stall_id}から/reviews//stall/{stall_id}に変更
@router.get("/reviews/stall/{stall_id}", response_model=List[ReviewResponse])
def get_reviews_by_stall_id(stall_id: int):
    try:
        
        reviews = Review.get_by_stall_id(stall_id)
        return reviews
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ユーザーidからレビューリスト取得エンドポイント
## /reviews/{user_id}から/reviews/user/{user_id}に変更
@router.get("/reviews/user/{user_id}", response_model=List[ReviewResponse])
def get_reviews_by_user_id(user_id: int):
    try:
        
        reviews = Review.get_list_by_user_id(user_id)
        return reviews
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# レビューの平均値のランキングtop3取得するエンドポイント
@router.get("/reviews/top-ranking", response_model=Reviewranking)
def get_rating_ranking():
    try:
        all_reviews = Review.get_list()
        stall_rating = {}
        
        for review in all_reviews:
            if review.stall_id not in stall_rating:
                stall_rating[review.stall_id] = []
            stall_rating[review.stall_id].append(review.rating)
        
        average_ratings = {}
        for stall_id, ratings in stall_rating.items():
            if len(ratings) < 3:
                continue
            average_ratings[stall_id] = sum(ratings) / len(ratings)
        
        sorted_stalls = sorted(average_ratings.items(), key=lambda x: x[1], reverse=True)[:3]
        
        ranking_list = [StallResponse.from_orm(Stall.get_by_id(stall_id)) for stall_id, _ in sorted_stalls]
        
        return Reviewranking(ranking=ranking_list)  # Reviewrankingとして返す
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 店舗idのレビューの平均評価、レビュー件数、それぞれの星の数を取得するエンドポイント
@router.get("/reviews/average/{stall_id}")
def get_average_rating(stall_id: int):
    try:
        all_reviews = Review.get_by_stall_id(stall_id)
        average_rating = sum([review.rating for review in all_reviews]) / len(all_reviews)
        rating_count = len(all_reviews)
        rating_distribution = [0, 0, 0, 0, 0]
        for review in all_reviews:
            rating_distribution[review.rating - 1] += 1
        return {
            "average_rating": average_rating,
            "rating_count": rating_count,
            "rating_distribution": rating_distribution
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# レビューの削除エンドポイント
@router.delete("/reviews/{review_id}")
def delete_review(review_id: int):
    try:
        Review.delete(review_id)
        return JSONResponse({'is_success': True})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
