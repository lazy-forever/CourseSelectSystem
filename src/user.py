from entity.Select import Select
from entity.Course import Course
import runSql

def user_loginSql(num, password):
    sql = "select * from students where num = '%s' and password = '%s'" % (num, password)
    result = runSql.runSql(sql)
    if len(result) == 0:
        return False
    return True

def select_courseSql(num, code):
    sql = "insert into selects values ('%s', '%s', null)" % (num, code)
    try:
        runSql.runSql(sql)
    except Exception as e:
        print(e)
        return False
    return True

def info_showSql(num):
    sql = '''
SELECT c.code, c.name AS course_name, c.credit, t.name AS teacher_name, s.score
FROM students stu
JOIN selects s ON stu.num = s.num
JOIN course c ON s.code = c.code
JOIN teachers t ON c.num = t.num
WHERE stu.num = %s;'''%num
    result = runSql.runSql(sql)
    courses = []
    for row in result:
        course = Course(row[0], row[1], row[2], row[3])
        courses.append(course)
    selects = []
    for course in courses:
        select = Select(course, row[4])
        selects.append(select)
    return selects

def delete_selectSql(num, code):
    sql = "delete from selects where num = %s and code = '%s';" % (num, code)
    try:
        print(runSql.runSql(sql))
    except Exception as e:
        print(e)
        return False
    return True