from datetime import datetime, time
from sqlalchemy.orm import Session
from app.db.session import engine, SessionLocal
from app.db.base import Base, ProgressStatus, PathStatus

# Import tất cả các Model
from app.model.user import User
from app.model.skill import Skill, GoalSkill, UserSkill
from app.model.career_goal import CareerGoal
from app.model.course import Course, CourseSkill, CoursePrerequisite
# Giả sử file chứa model Lesson tên là lesson.py
from app.model.lesson import Lesson, LessonProgress
# Giả sử file chứa model LearningPath tên là learning_path.py
from app.model.learning_path import LearningPath, PathNode
# Giả sử file chứa model PersonalSchedule tên là personal_schedule.py
from app.model.personal_schedule import PersonalSchedule

from app.core.security import get_password_hash


def reset_database():
    """Xóa sạch DB cũ và tạo lại DB mới"""
    print("⚠️  Đang xóa toàn bộ bảng dữ liệu cũ...")
    Base.metadata.drop_all(bind=engine)

    print("✅ Đang tạo lại cấu trúc bảng mới...")
    Base.metadata.create_all(bind=engine)


def seed_data(db: Session):
    print("⏳ Đang bơm dữ liệu mẫu (Seed Data)...")

    # ==========================================
    # 1. TẠO DỮ LIỆU GỐC (Không phụ thuộc khóa ngoại)
    # ==========================================

    # --- Users ---
    admin_user = User(username="admin", email="admin@gmail.com", password_hash=get_password_hash("123456"))
    student_1 = User(username="sv1", email="mymy@gmail.com", password_hash=get_password_hash("123456"))
    student_2 = User(username="sv2", email="momi@gmail.com", password_hash=get_password_hash("123456"))
    student_3 = User(username="sv3", email="giabao@gmail.com", password_hash=get_password_hash("123456"))

    db.add_all([admin_user, student_1, student_2, student_3])

    # --- Skills ---
    python = Skill(name="Python")
    sql = Skill(name="SQL & Database Verification")
    testing = Skill(name="Unit Testing & Coverage")
    cv = Skill(name="Computer Vision (CNN, Mamba)")

    db.add_all([python, sql, testing, cv])

    # --- Career Goals ---
    tester_goal = CareerGoal(title="Software Tester",
                             description="Chuyên viên kiểm thử phần mềm, đảm bảo chất lượng hệ thống.")
    ai_goal = CareerGoal(title="AI Engineer", description="Kỹ sư Trí tuệ nhân tạo, phát triển các mô hình học sâu.")

    db.add_all([tester_goal, ai_goal])

    # Bắt buộc Commit lần 1 để DB sinh ra các ID (user.id, skill.id, goal.id)
    db.commit()

    # ==========================================
    # 2. TẠO DỮ LIỆU CẤP 2 (Khóa học & Liên kết mục tiêu)
    # ==========================================

    # --- Goal - Skill ---
    db.add_all([
        GoalSkill(goal_id=tester_goal.id, skill_id=testing.id, weight=5),
        GoalSkill(goal_id=tester_goal.id, skill_id=sql.id, weight=4),
        GoalSkill(goal_id=tester_goal.id, skill_id=python.id, weight=3),

        GoalSkill(goal_id=ai_goal.id, skill_id=cv.id, weight=5),
        GoalSkill(goal_id=ai_goal.id, skill_id=python.id, weight=5),
    ])

    # --- Courses ---
    course_python = Course(title="Lập trình Python Căn Bản", description="Nền tảng Python cho mọi ngành nghề.",
                           estimated_hours=20)
    course_testing = Course(title="Kiểm thử tự động & Unit Test",
                            description="Viết test case, đo coverage và verify database.", estimated_hours=35)
    course_alpr = Course(title="Xây dựng hệ thống ALPR", description="Nhận dạng biển số xe bằng AI.",
                         estimated_hours=40)

    db.add_all([course_python, course_testing, course_alpr])
    db.commit()  # Lấy ID cho Courses

    # ==========================================
    # 3. TẠO DỮ LIỆU CẤP 3 (Chi tiết khóa học & Bài học)
    # ==========================================

    # --- Course Prerequisites (Khóa học tiên quyết) ---
    db.add(CoursePrerequisite(course_id=course_testing.id, prerequisite_course_id=course_python.id))
    db.add(CoursePrerequisite(course_id=course_alpr.id, prerequisite_course_id=course_python.id))

    # --- Course - Skill ---
    db.add_all([
        CourseSkill(course_id=course_python.id, skill_id=python.id),
        CourseSkill(course_id=course_testing.id, skill_id=testing.id),
        CourseSkill(course_id=course_testing.id, skill_id=sql.id),
        CourseSkill(course_id=course_alpr.id, skill_id=cv.id),
    ])

    # --- Lessons ---
    lesson_1 = Lesson(course_id=course_python.id, title="Cài đặt môi trường", content_type="Video",
                      duration_seconds=600, sequence_order=1)
    lesson_2 = Lesson(course_id=course_python.id, title="Cú pháp cơ bản", content_type="Video", duration_seconds=1200,
                      sequence_order=2)
    lesson_3 = Lesson(course_id=course_testing.id, title="Viết Unit Test đầu tiên", content_type="Reading",
                      duration_seconds=900, sequence_order=1)

    db.add_all([lesson_1, lesson_2, lesson_3])
    db.commit()  # Lấy ID cho Lesson

    # ==========================================
    # 4. TẠO DỮ LIỆU TƯƠNG TÁC NGƯỜI DÙNG (Cá nhân hóa)
    # ==========================================

    # --- User Skills (Kỹ năng đã có của Mơ Mi) ---
    db.add(UserSkill(user_id=student_2.id, skill_id=python.id, proficiency_level=3))

    # --- Learning Path (Lộ trình học của Mơ Mi) ---
    path_momi = LearningPath(user_id=student_2.id, career_goal_id=tester_goal.id, status=PathStatus.ACTIVE)
    db.add(path_momi)
    db.commit()

    # --- Path Nodes (Các chặng đường trong lộ trình) ---
    db.add_all([
        PathNode(learning_path_id=path_momi.id, course_id=course_python.id, sequence_order=1, is_unlocked=True,
                 status=ProgressStatus.COMPLETED),
        PathNode(learning_path_id=path_momi.id, course_id=course_testing.id, sequence_order=2, is_unlocked=True,
                 status=ProgressStatus.IN_PROGRESS)
    ])

    # --- Lesson Progress (Tiến độ bài học) ---
    db.add(LessonProgress(
        user_id=student_2.id, lesson_id=lesson_1.id,
        status=ProgressStatus.COMPLETED, watched_seconds=600,
        started_at=datetime.now(), completed_at=datetime.now()
    ))

    # --- Personal Schedule (Lịch học cá nhân) ---
    # Lịch học vào Thứ 3 (day_of_week=3) từ 19:00 đến 21:00
    db.add(PersonalSchedule(
        user_id=student_2.id, course_id=course_testing.id,
        day_of_week=3, start_time=time(19, 0), end_time=time(21, 0), is_reminder_enabled=True
    ))

    # Lưu toàn bộ thay đổi cuối cùng
    db.commit()
    print("🎉 Hoàn tất! Database đã sẵn sàng với đầy đủ bảng và dữ liệu liên kết.")


if __name__ == "__main__":
    reset_database()
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()