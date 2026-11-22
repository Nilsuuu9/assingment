import sys, pytest
sys.path.insert(0, "src")
from datetime import date
from school import Student, Teacher, Department, Course, Person


def make_student():
    return Student("S1", "Ali", "Demir", date(2004, 3, 12))


def test_person_is_abstract():
    with pytest.raises(TypeError):
        Person("a", "b", date(2000, 1, 1))


def test_enroll_and_gpa():
    s = make_student()
    c1, c2 = Course("A", "A", 4), Course("B", "B", 2)
    s.enroll(c1).set_grade("AA")
    s.enroll(c2).set_grade("CC")
    assert s.gpa() == pytest.approx(3.33, abs=0.01)


def test_duplicate_enrollment():
    s, c = make_student(), Course("A", "A", 3)
    s.enroll(c)
    with pytest.raises(ValueError):
        s.enroll(c)


def test_capacity_and_drop():
    c = Course("A", "A", 3, capacity=1)
    s1, s2 = make_student(), make_student()
    s1.enroll(c)
    with pytest.raises(ValueError):
        s2.enroll(c)
    s1.drop(c)
    assert not c.is_full()


def test_invalid_grade():
    s, c = make_student(), Course("A", "A", 3)
    with pytest.raises(ValueError):
        s.enroll(c).set_grade("ZZ")


def test_department_and_teacher():
    d = Department("CE")
    s = Student("S1", "A", "B", date(2004, 1, 1), department=d)
    t = Teacher("T1", "C", "D", date(1980, 1, 1))
    c = Course("X", "X", 3)
    d.add_course(c); t.assign(c)
    assert s in d.students and c.teacher is t and c in t.courses
