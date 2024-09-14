from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from api.database.models import Stall  # 屋台モデル
from pydantic import BaseModel

router = APIRouter()

# Stallスキーマ（屋台）
class StallBase(BaseModel):
    stall_name: str
    owner_name: str
    thumbnail_URL: str


class StallCreate(StallBase):
    pass


class StallResponse(StallBase):
    id: int



# 屋台の作成エンドポイント
@router.post("/stalls/")
def create_stall(stall: StallCreate):
    return JSONResponse({'is_success': Stall.create(stall_name=stall.stall_name, owner_name=stall.owner_name, thumbnail_URL=stall.thumbnail_URL)})

# 屋台リスト取得エンドポイント
@router.get("/stalls/", response_model=List[StallResponse])
def get_stalls():
    try:
        # Stallテーブルから全レコードを取得
        stalls = Stall.get_list()
        return stalls
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
