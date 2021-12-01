from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from orm.base import Base
import orm.models

engine = create_engine("sqlite:///test_db3.sqlite3", echo=False)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)