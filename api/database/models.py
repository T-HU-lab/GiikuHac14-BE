from sqlalchemy import Column, Integer, String, ForeignKey, Text, TIMESTAMP, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from api.database.db import Session as db_session
import logging

from api.database.db import ModelBase

# ロガーの設定
logger = logging.getLogger(__name__)

# Stallモデル（屋台）
class Stall(ModelBase):
    __tablename__ = "stalls"

    id = Column(Integer, primary_key=True, index=True)
    stall_name = Column(String(100), nullable=False)
    owner_name = Column(String(100), nullable=False)
    thumbnail_URL = Column(String(200), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # StallとItem、Reviewのリレーション
    items = relationship("Item", back_populates="stall")
    reviews = relationship("Review", back_populates="stall")
    
    @classmethod
    def create(
        cls, stall_name: str, owner_name: str, thumbnail_URL: str = None
    ):
        try:
            new_stall = cls(stall_name=stall_name, owner_name=owner_name, thumbnail_URL=thumbnail_URL)
            db_session.add(new_stall)
            db_session.commit()
            return True
        except Exception as e:
            db_session.rollback()
            logger.error(f"Failed to create stall: {e}")
            return False

    @classmethod
    def get_list(cls):
        return db_session.query(cls).all()

    @classmethod
    def get_by_id(cls, stall_id: int):
        return db_session.query(cls).filter(cls.id == stall_id).first()
    
    @classmethod
    def get_by_owner_name(cls, owner_name: str):
        return db_session.query(cls).filter(cls.owner_name == owner_name).first()

    @classmethod
    def get_by_stall_name(cls, stall_name: str):
        return db_session.query(cls).filter(cls.stall_name == stall_name).first()
    
    @classmethod
    def update_thumbnail_URL(cls, stall_id: int, thumbnail_URL: str):
        try:
            db_session.query(cls).filter(cls.id == stall_id).update({cls.thumbnail_URL: thumbnail_URL})
            db_session.commit()
            return True
        except Exception as e:
            db_session.rollback()
            logger.error(f"Failed to update thumbnail URL: {e}")
            return False


# Itemモデル（品物）
class Item(ModelBase):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    stall_id = Column(Integer, ForeignKey("stalls.id"), nullable=False)
    item_name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # ItemとStallのリレーション
    stall = relationship("Stall", back_populates="items")

    @classmethod
    def get_list(cls):
        return db_session.query(cls).all()
    
    @classmethod
    def create(
        cls, stall_id: int, item_name: str, price: int 
    ):
        try:
            new_item = cls(stall_id=stall_id, item_name=item_name, price=price)
            db_session.add(new_item)
            db_session.commit()
            return True
        except Exception as e:
            db_session.rollback()
            logger.error(f"Failed to create stall: {e}")
            return False
    
    @classmethod
    def get_by_id(cls, item_id: int):
        return db_session.query(cls).filter(cls.id == item_id).first()

    @classmethod
    def get_list_by_stall_id(cls, stall_id: int):
        return db_session.query(cls).filter(cls.stall_id == stall_id).all()
    
    @classmethod
    def get_by_item_name(cls, item_name: str):
        return db_session.query(cls).filter(cls.item_name == item_name).first()


# Userモデル（ユーザー）
class User(ModelBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # UserとReviewのリレーション
    reviews = relationship("Review", back_populates="user")
    
    @classmethod
    def create(
        cls, username: str, password: str, email: str 
    ):
        try:
            new_user = cls(username=username, password=password, email=email)
            db_session.add(new_user)
            db_session.commit()
            return True
        except Exception as e:
            db_session.rollback()
            logger.error(f"Failed to create stall: {e}")
            return False

    @classmethod
    def get_list(cls):
        return db_session.query(cls).all()
    
    @classmethod
    def get_by_username(cls, username: str):
        return db_session.query(cls).filter(cls.username == username).first()

    @classmethod
    def get_by_email(cls, email: str):
        return db_session.query(cls).filter(cls.email == email).first()

    @classmethod
    def get_by_id(cls, user_id: int):
        return db_session.query(cls).filter(cls.id == user_id).first()
    
    @classmethod
    def authenticate(cls, username: str, password: str):
        return db_session.query(cls).filter(cls.username == username, cls.password == password).first()
    

# Reviewモデル（レビュー）
class Review(ModelBase):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    stall_id = Column(Integer, ForeignKey("stalls.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    

    # ReviewとStall、Userのリレーション
    stall = relationship("Stall", back_populates="reviews")
    user = relationship("User", back_populates="reviews")

    @classmethod
    def create(
        cls, stall_id: int, user_id: int, rating: int, comment: str
    ):
        try:
            new_review = cls(stall_id=stall_id, user_id=user_id, rating=rating, comment=comment)
            db_session.add(new_review)
            db_session.commit()
            
            # ここでTrueではなく、作成したオブジェクトを返す
            return new_review
        except Exception as e:
            db_session.rollback()
            logger.error(f"Failed to create review: {e}")
            return None  # 失敗時はNoneを返すようにする
    
    @classmethod
    def get_list(cls):
        return db_session.query(cls).all()

    @classmethod
    def get_by_id(cls, review_id: int):
        return db_session.query(cls).filter(cls.id == review_id).first()

    @classmethod
    def get_list_by_user_id(cls, user_id: int):
        return db_session.query(cls).filter(cls.user_id == user_id).all()

    @classmethod
    def get_by_stall_id(cls, stall_id: int):
        return db_session.query(cls).filter(cls.stall_id == stall_id).all()