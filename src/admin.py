from entity.Course import Course
from entity.Choose import Choose
from entity.Student import Student
import runSql

def admin_loginSql(num, password):
    sql = "select * from teachers where num = '%s' and password = '%s'" % (num, password)
    result = runSql.runSql(sql)
    if len(result) == 0:
        return False
    return True

def courses_showSql():
    # return all courses
    sql = "SELECT c.code, c.name AS course_name, c.credit, t.name AS teacher_name FROM course c JOIN teachers t ON c.num = t.num;"
    result = runSql.runSql(sql)
    courses = []
    for row in result:
        course = Course(row[0], row[1], row[2], row[3])
        courses.append(course)
    return courses

def course_showSql(code):
    sql = "SELECT c.code, c.name AS course_name, c.credit, t.name AS teacher_name FROM course c JOIN teachers t ON c.num = t.num WHERE c.code = '%s';" % code
    result = runSql.runSql(sql)
    if len(result) == 0:
        return None
    row = result[0]
    course = Course(row[0], row[1], row[2], row[3])
    return course

def course_editorSql(code, name, credit):
    sql = "update course set name = '%s', credit = %s where code = '%s';" % (name, credit, code)
    try:
        runSql.runSql(sql)
    except Exception as e:
        print(e)
        return False
    return True

def mycourses_showSql(num):
    sql = "SELECT c.code, c.name AS course_name, c.credit, t.name AS teacher_name FROM course c JOIN teachers t ON c.num = t.num WHERE c.num = '%s';" % num
    result = runSql.runSql(sql)
    courses = []
    for row in result:
        course = Course(row[0], row[1], row[2], row[3])
        courses.append(course)
    return courses

def delete_courseSql(code):
    sql = "delete from course where code = '%s';" % code
    try:
        runSql.runSql(sql)
    except Exception as e:
        print(e)
        return False
    return True

def choose_showSql(code):
    # return a course of all student
    sql = "SELECT s.num, s.name, c.name, c.code, se.score FROM students s JOIN selects se ON s.num = se.num JOIN course c ON se.code = c.code WHERE c.code = '%s';" % code
    result = runSql.runSql(sql)
    chooses = []
    for row in result:
        student = Student(row[0], row[1])
        choose = Choose(student, row[2], row[3], row[4])
        chooses.append(choose)
    return chooses

def course_addSql(code, name, credit, num):
    sql = "insert into course values ('%s', '%s', %s, '%s')" % (code, name, credit, num)
    try:
        runSql.runSql(sql)
    except Exception as e:
        print(e)
        return False
    return True

def edit_scoreSql(num, code, score):
    # edit a student's score
    sql = "update selects set score = %s where num = '%s' and code = '%s';" % (score, num, code)
    try:
        runSql.runSql(sql)
    except Exception as e:
        print(e)
        return False
    return True

def registerSql(num, name, password):
    # register a student
    sql = "insert into students values ('%s', '%s', '%s')" % (num, name, password)
    try:
        runSql.runSql(sql)
    except Exception as e:
        print(e)
        return False
    return True