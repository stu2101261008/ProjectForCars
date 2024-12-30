from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL за връзка с базата данни
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Заменете с вашата база данни

# Създаване на двигател за връзка с базата данни
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Създаване на сесии за взаимодействие с базата данни
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базов клас за моделите
Base = declarative_base()

# Функция за получаване на сесия към базата данни
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
