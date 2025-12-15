from .config import Settigs
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import declarative_base, DeclarativeBase, sessionmaker

settings = Settigs()
url = URL.create(
    drivername='postgresql+psycopg2',
    username=settings.DB_USER,
    password=settings.DB_PASS,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.DB_NAME
)

engine = create_engine(url=url)
Base: DeclarativeBase = declarative_base()
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()