from entity.Select import Select
from entity.Course import Course
from entity.Student import Student
from entity.Teacher import Teacher
from entity.Project import Project
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

def projects_showSql(num):
    sql = 'select s.name, t.num, t.name, p.name, p.imgurl, p.url, p.status, p.id from projects p join students s on p.snum = s.num join teachers t on p.tnum = t.num where s.num = %s;'%num
    try:
        result = runSql.runSql(sql)
        projects = []
        for row in result:
            student = Student(num, row[0])
            teacher = Teacher(row[1], row[2])
            project = Project(student, teacher, row[3], row[4], row[5], row[6], row[7])
            projects.append(project)
    except Exception as e:
        print(e)
        return []
    return projects

def exit_projectSql(num, id):
    sql = 'delete from projects where snum = %s and id = %s'%(num,id)
    try:
        print(runSql.runSql(sql))
    except Exception as e:
        print(e)
        return False
    return True

def edit_projectSql(num, id, name, imgurl, url):
    sql = "update projects set name = '%s', imgurl = '%s', url = '%s' where snum = %s and id = %s;" % (name, imgurl, url, num, id)
    try:
        runSql.runSql(sql)
    except Exception as e:
        print(e)
        return False
    return True