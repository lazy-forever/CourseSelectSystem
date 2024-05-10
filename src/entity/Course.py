class Course:
    def __init__(self,  code='123', name='name',credit=2, teacher='test'):
        '''
        name: 课程名
        code: 课程代码
        credit: 学分
        teacher: 教师
        '''
        self.name = name
        self.code = code
        self.credit = credit
        self.teacher = teacher

    def __str__(self):
        return f"Course: {self.name} ({self.code}) - {self.credit} credits"