import sys
sys.path.insert(0, "src")
from datetime import date
from school import Address, Student, Teacher, Department, Course

cs = Department("Computer Engineering")
teacher = Teacher("T001", "Ayşe", "Yılmaz", date(1980, 5, 17), department=cs)
oop = Course("CENG201", "Object Oriented Programming", credits=4)
db = Course("CENG301", "Databases", credits=3)
for c in (oop, db):
    cs.add_course(c)
    teacher.assign(c)

ali = Student("S1001", "Ali", "Demir", date(2004, 3, 12),
              Address("Atatürk Cad. 10", "Mersin"), cs)
ali.enroll(oop).set_grade("AA")
ali.enroll(db).set_grade("BB")

print(ali, "|", ali.address)
print("Courses:", [e.course.name for e in ali.enrollments])
print("GPA:", ali.gpa())
print(teacher, "teaches", [c.code for c in teacher.courses])
