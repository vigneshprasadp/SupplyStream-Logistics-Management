from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Database_url = "mysql+pymysql://root:vignesh51##@localhost/logistics_db"

engine = create_engine(Database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()