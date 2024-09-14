from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from api.database.models import Item  # 屋台モデル
from pydantic import BaseModel

router = APIRouter()


# Itemスキーマ（品物）
class ItemBase(BaseModel):
    stall_id: int
    item_name: str
    price: int


class ItemCreate(ItemBase):
    pass


class ItemResponse(ItemBase):
    id: int

    class Config:
        from_attributes = True  # Pydantic v2 でORM対応

# 商品の作成エンドポイント
@router.post("/items/")
def create_item(item: ItemCreate):
    return JSONResponse({'is_success': Item.create(stall_id=item.stall_id, item_name=item.item_name, price=item.price)})

# 商品リスト取得エンドポイント
@router.get("/items/", response_model=List[ItemResponse])
def get_item():
    try:
        # Itemテーブルから全レコードを取得
        items = Item.get_list()
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 店idから商品リストを取得
@router.get("/items/{stall_id}", response_model=List[ItemResponse])
def get_item_by_stall_id(stall_id: int):
    try:
        # Itemテーブルから全レコードを取得
        items = Item.get_list_by_stall_id(stall_id=stall_id)
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))