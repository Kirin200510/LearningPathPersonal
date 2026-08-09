from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.core.security import get_password_hash

# Import tất cả model để SQLAlchemy biết metadata
from app.model.user import User
from app.model.skill import Skill, UserSkill, GoalSkill
from app.model.course import Course, CourseSkill, CoursePrerequisite
from app.model.career_goal import CareerGoal
from app.model.learning_path import LearningPath, PathNode
from app.model.personal_schedule import PersonalSchedule


TEST_USERNAME = "testuser"
TEST_EMAIL = "testuser@gmail.com"
TEST_PASSWORD = "123456"


def seed_db():
    # =========================
    # 1. Reset database
    # =========================
    print("Dropping old database tables...")
    Base.metadata.drop_all(bind=engine)

    print("Creating new database tables...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # =========================
        # 2. Tạo user test
        # =========================
        user = User(
            username=TEST_USERNAME,
            email=TEST_EMAIL,
            password_hash=get_password_hash(TEST_PASSWORD),
            avatar="default.jpg",
            is_active=True,
        )

        db.add(user)
        db.flush()

        # =========================
        # 3. Tạo skills
        # =========================
        skill_names = [
            "Python",
            "Java",
            "SQL",
            "Git",
            "FastAPI",
            "Docker",
            "HTML",
            "CSS",
            "JavaScript",
        ]

        skills = {}

        for skill_name in skill_names:
            skill = Skill(name=skill_name)

            db.add(skill)
            db.flush()

            skills[skill_name] = skill

        # =========================
        # 4. Known skills của user
        # =========================
        known_skills = {
            "Python": 4,
            "Git": 3,
        }

        for skill_name, level in known_skills.items():
            user_skill = UserSkill(
                user_id=user.id,
                skill_id=skills[skill_name].id,
                proficiency_level=level,
            )

            db.add(user_skill)

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