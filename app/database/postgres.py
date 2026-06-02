from sqlalchemy import create_engine, Column, String, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.config import settings

engine = create_engine(
    settings.DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class MonitoredTarget(Base):
    __tablename__ = "monitored_targets"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, default="N/A")
    biography = Column(String, default="")
    profile_pic_url = Column(String, default="")
    is_private = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    follower_count_cache = Column(Integer, default=0)
    following_count_cache = Column(Integer, default=0)
    posts_count_cache = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    last_checked = Column(DateTime, default=datetime.utcnow)

def init_pg_db():
    Base.metadata.create_all(bind=engine)

