from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from settings import settings

# Create a SQLAlchemy engine
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session class for database interactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models
Base = declarative_base()

# Define the Any model here model
class ExampleModel(Base):
    __tablename__ = "example_model"

    id = Column(Integer, primary_key=True, index=True)
    example_id = Column(Integer, index=True)
    example_timestamp = Column(DateTime, default=datetime.utcnow)
    example = Column(String)

# Create the database and tables
Base.metadata.create_all(bind=engine)

