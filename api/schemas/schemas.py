from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# Itemスキーマ（品物）
class ItemBase(BaseModel):
    item_name: str
    price: float


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    item_id: int
    stall_id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Userスキーマ（ユーザー）
class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True
        
# Reviewスキーマ（レビュー）
class ReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)  # 1〜5の範囲でバリデーション
    comment: str


class ReviewCreate(ReviewBase):
    stall_id: int
    user_id: int


class Review(ReviewBase):
    review_id: int
    stall_id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Stallスキーマ（屋台）
class StallBase(BaseModel):
    name: str
    owner_name: str
    thumbnail_URL: Optional[str] = None


class StallCreate(StallBase):
    pass


class Stall(StallBase):
    stall_id: int
    created_at: datetime
    items: List[Item] = []
    reviews: List[Review] = []

    class Config:
        orm_mode = True
