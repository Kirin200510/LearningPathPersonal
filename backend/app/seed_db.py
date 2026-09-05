from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.core.security import get_password_hash

# Import các model còn sử dụng
from app.model.user import User
from app.model.course import Course
from app.model.learning_path import LearningPath, PathNode
from app.model.personal_schedule import PersonalSchedule


TEST_USERNAME = "testuser"
TEST_EMAIL = "testuser@gmail.com"
TEST_PASSWORD = "123456"


def seed_db():

    print("Dropping old database tables...")
    Base.metadata.drop_all(bind=engine)

    print("Creating new database tables...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        user = User(
            username=TEST_USERNAME,
            email=TEST_EMAIL,
            password_hash=get_password_hash(
                TEST_PASSWORD
            ),
            avatar="default.jpg",
            is_active=True,
        )

        db.add(user)
        db.commit()

        print()
        print("===== SEED COMPLETED =====")
        print(f"Username: {TEST_USERNAME}")
        print(f"Password: {TEST_PASSWORD}")
        print("==========================")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_db()