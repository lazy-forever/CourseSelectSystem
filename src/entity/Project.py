from entity.Student import Student
from entity.Teacher import Teacher

class Project:
    def __init__(self, student=Student(), teacher=Teacher(), name='testProject', imgurl='testProject.jpg', url='testProject.html', status='未申报', id=None):
        '''
        student: 学生
        Teacher: 教师
        name: 项目名称
        imgurl: 项目图片
        url: 项目链接
        status: 项目状态
        '''
        self.student = student
        self.teacher = teacher
        self.name = name
        self.imgurl = imgurl
        self.url = url
        self.status = status
        self.id = id