class Schedule:

    def __init__(self, day):
        sessions = None
        time = None
        student_count = 0
        instructors = []

    def fully_staffed(self):
        return self.student_count <= self.students_per_instructor *len(self.instructors)

    def add_instructor(self, instructor):
        return self.instructors.append(instructor)