from entity.Student import Student

class Choose:
    def __init__(self, student=Student(), name='test', code='123', score=0):
        self.student = student
        self.name = name
        self.code = code
        self.score = score