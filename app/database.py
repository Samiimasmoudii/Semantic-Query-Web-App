from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import Config  # Import your config class for consistency

# Define the SQLAlchemy base
Base = declarative_base()

# Retrieve the database URL from Config
DATABASE_URL = Config.SQLALCHEMY_DATABASE_URI

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True, pool_size=10, max_overflow=20)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize the database connection and session
def get_db():
    """
    Dependency to get the database session.
    """
    db = SessionLocal()  # Create the session
    try:
        yield db  # This will be used in route functions to get a session
    finally:
        db.close()  # Ensure the session is closed after use

# To create tables (useful for first-time setup)
def create_tables():
    """
    Creates all tables in the database. This is called once during setup.
    """
    Base.metadata.create_all(bind=engine)
