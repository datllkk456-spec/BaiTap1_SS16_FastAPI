from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# Bảng trung gian Student - Course
student_course = Table(
    "student_course",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True)
)


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    # ===== LỖI 1 (Quan hệ 1-N) =====
    # Code cũ:
    # students = relationship("Student", back_populates="department_id")
    #
    # Nguyên nhân:
    # department_id là khóa ngoại (Column), không phải relationship.
    # back_populates phải tham chiếu đến thuộc tính relationship ở model Student.
    #
    # Cách sửa:
    # back_populates="department"
    students = relationship("Student", back_populates="department")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)

    department_id = Column(Integer, ForeignKey("departments.id"))

    department = relationship(
        "Department",
        back_populates="students"
    )

    # ===== LỖI 2 (Quan hệ 1-1) =====
    # Code cũ:
    # profile = relationship("Profile", back_populates="student")
    #
    # Nguyên nhân:
    # Không có uselist=False nên SQLAlchemy hiểu đây là quan hệ 1-N.
    #
    # Cách sửa:
    # Thêm uselist=False để mỗi Student chỉ có một Profile.
    profile = relationship(
        "Profile",
        back_populates="student",
        uselist=False
    )

    # ===== LỖI 3 (Quan hệ N-N) =====
    # Code cũ:
    # courses = relationship("Course", back_populates="students")
    #
    # Nguyên nhân:
    # Thiếu secondary=student_course nên SQLAlchemy
    # không biết sử dụng bảng trung gian nào.
    #
    # Cách sửa:
    # Thêm secondary=student_course.
    courses = relationship(
        "Course",
        secondary=student_course,
        back_populates="students"
    )


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    bio = Column(String(255))

    # ===== Sửa cho quan hệ 1-1 =====
    # Code cũ:
    # student_id = Column(Integer, ForeignKey("students.id"))
    #
    # Nguyên nhân:
    # Thiếu unique=True nên nhiều Profile có thể cùng tham chiếu
    # đến một Student.
    #
    # Cách sửa:
    # Thêm unique=True để đảm bảo 1 Student chỉ có 1 Profile.
    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        unique=True
    )

    student = relationship(
        "Student",
        back_populates="profile"
    )


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)

    # ===== Sửa cho quan hệ N-N =====
    # Thêm secondary=student_course để liên kết qua bảng trung gian.
    students = relationship(
        "Student",
        secondary=student_course,
        back_populates="courses"
    )