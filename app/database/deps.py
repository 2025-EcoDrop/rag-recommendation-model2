import os

IS_TEST = os.getenv("TEST_ENV") == "true"

if not IS_TEST:
    from app.database.database import SessionLocal

    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()