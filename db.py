from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

DB_URL = "sqlite:///data/app.db"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class PromptLog(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(String)
    prompt = Column(Text)
    output = Column(Text)
    model = Column(String)

def init_db():
    Base.metadata.create_all(bind=engine)
