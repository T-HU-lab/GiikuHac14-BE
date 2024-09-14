from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session

# 同期処理用のデータベースURL
DB_URL = "mysql://root@db:3306/demo?charset=utf8"

# 同期用のエンジンを作成
engine = create_engine(DB_URL, echo=True)
# 同期用のセッションを作成
Session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
# モデルのベースクラス
ModelBase = declarative_base()
