"""Student class diagram -> Python implementation."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date
from typing import Optional

GRADE_POINTS = {"AA": 4.0, "BA": 3.5, "BB": 3.0, "CB": 2.5, "CC": 2.0,
                "DC": 1.5, "DD": 1.0, "FF": 0.0}


@dataclass
class Address:
    """Composition: an Address cannot exist without its Person."""
    street: str
    city: str
    country: str = "Türkiye"

    def __str__(self) -> str:
        return f"{self.street}, {self.city}, {self.country}"


class Person(ABC):
    def __init__(self, first_name: str, last_name: str,
                 birth_date: date, address: Optional[Address] = None):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.address = address

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def age(self, today: Optional[date] = None) -> int:
        today = today or date.today()
        years = today.year - self.birth_date.year
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            years -= 1
        return years

    @abstractmethod
    def get_role(self) -> str: ...

    def __str__(self) -> str:
        return f"{self.get_role()}: {self.full_name}"


class Student(Person):
    def __init__(self, student_id: str, first_name: str, last_name: str,
                 birth_date: date, address: Optional[Address] = None,
                 department: Optional["Department"] = None):
        super().__init__(first_name, last_name, birth_date, address)
        self.student_id = student_id
        self.department = department
        self.enrollments: list[Enrollment] = []
        if department:
            department.add_student(self)

    def get_role(self) -> str:
        return "Student"

    def enroll(self, course: "Course") -> "Enrollment":
        if any(e.course is course for e in self.enrollments):
            raise ValueError(f"{self.full_name} is already enrolled in {course.code}")
        if course.is_full():
            raise ValueError(f"{course.code} is full")
        enrollment = Enrollment(self, course)
        self.enrollments.append(enrollment)
        course.enrollments.append(enrollment)
        return enrollment

    def drop(self, course: "Course") -> None:
        enrollment = next((e for e in self.enrollments if e.course is course), None)
        if enrollment is None:
            raise ValueError(f"{self.full_name} is not enrolled in {course.code}")
        self.enrollments.remove(enrollment)
        course.enrollments.remove(enrollment)

    def gpa(self) -> float:
        graded = [e for e in self.enrollments if e.grade is not None]
        credits = sum(e.course.credits for e in graded)
        if credits == 0:
            return 0.0
        points = sum(GRADE_POINTS[e.grade] * e.course.credits for e in graded)
        return round(points / credits, 2)


class Teacher(Person):
    def __init__(self, employee_id: str, first_name: str, last_name: str,
                 birth_date: date, address: Optional[Address] = None,
                 department: Optional["Department"] = None):
        super().__init__(first_name, last_name, birth_date, address)
        self.employee_id = employee_id
        self.department = department
        self.courses: list[Course] = []

    def get_role(self) -> str:
        return "Teacher"

    def assign(self, course: "Course") -> None:
        course.teacher = self
        if course not in self.courses:
            self.courses.append(course)


@dataclass
class Department:
    name: str
    students: list[Student] = field(default_factory=list)
    courses: list["Course"] = field(default_factory=list)

    def add_student(self, student: Student) -> None:
        if student not in self.students:
            self.students.append(student)
        student.department = self

    def add_course(self, course: "Course") -> None:
        if course not in self.courses:
            self.courses.append(course)
        course.department = self


@dataclass(eq=False)
class Course:
    code: str
    name: str
    credits: int
    capacity: int = 30
    teacher: Optional[Teacher] = None
    department: Optional[Department] = None
    enrollments: list["Enrollment"] = field(default_factory=list)

    def is_full(self) -> bool:
        return len(self.enrollments) >= self.capacity

    def students(self) -> list[Student]:
        return [e.student for e in self.enrollments]


class Enrollment:
    """Association class between Student and Course."""

    def __init__(self, student: Student, course: Course):
        self.student = student
        self.course = course
        self.enrolled_on = date.today()
        self._grade: Optional[str] = None

    @property
    def grade(self) -> Optional[str]:
        return self._grade

    def set_grade(self, grade: str) -> None:
        if grade not in GRADE_POINTS:
            raise ValueError(f"Invalid grade: {grade}")
        self._grade = grade
