class Course:
    def __init__(self, name, start_date, number_of_lectures, teacher):
        self._name = name
        self._start_date = start_date
        self._number_of_lectures = number_of_lectures
        self._teacher = teacher
        self._students = []
        self._lectures = [Lecture(f'Lecture {i}', i, teacher)
                          for i in range(1, number_of_lectures + 1)]
        for lecture in self._lectures:
            self._teacher.assign(lecture)

    def __str__(self):
        return f"{self._name} ({self._start_date})"

    @property
    def teacher(self):
        return self._teacher

    @property
    def lectures(self):
        return self._lectures

    @property
    def number_of_lectures(self):
        return self._number_of_lectures

    def get_lecture(self, index):
        try:
            assert (index > 0) and (index <= self._number_of_lectures)
        except AssertionError:
            raise AssertionError('Invalid lecture number')
        return self._lectures[index - 1]

    def get_homeworks(self):
        return [lecture.get_homework()
                for lecture in self._lectures
                if lecture.get_homework() is not None]

    def enrolled_by(self):
        return self._students

    def enroll(self, new_student):
        if new_student is not None:
            self._students.append(new_student)


class Lecture:
    def __init__(self, name, number, teacher):
        self._name = name
        self._number = number
        self._teacher = teacher
        self._homework = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def number(self):
        return self._number

    @property
    def teacher(self):
        return self._teacher

    def new_teacher(self, new_teacher):
        if self._teacher:
            self._teacher.release(self)
        self._teacher = new_teacher
        new_teacher.assign(self)

    def get_homework(self):
        return self._homework

    def set_homework(self, homework):
        self._homework = homework


class Homework:
    def __init__(self, name, description):
        self._name = name
        self._description = description
        self._solutions = dict()

    def __str__(self):
        return f"{self._name}: {self._description}"

    @property
    def solutions(self):
        return self._solutions

    def done_by(self):
        return self._solutions


class Person:
    def __init__(self, first_name, last_name):
        self._first_name = first_name
        self._last_name = last_name

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def full_name(self):
        return f"{self._first_name} {self._last_name}"

    def __str__(self):
        return self.full_name


class Teacher(Person):
    def __init__(self, first_name, last_name):
        super().__init__(first_name, last_name)
        self._lectures = []

    def __str__(self):
        return f"Teacher: {self.full_name}"

    def assign(self, lecture):
        if lecture not in self._lectures:
            self._lectures.append(lecture)

    def release(self, lecture):
        self._lectures.remove(lecture)

    def teaching_lectures(self):
        return self._lectures

    @property
    def homeworks_to_check(self):
        homeworks = []
        for lecture in self._lectures:
            work = lecture.get_homework()
            if work is not None:
                if None in work.solutions.values():
                    homeworks.append(work)
        return homeworks

    def check_homework(self, homework, person, new_mark):
        if new_mark < 0 or new_mark > 100:
            raise AssertionError('Invalid mark')
        for lecture in self._lectures:
            work = lecture.get_homework()
            if work is homework:
                old_mark = work.solutions.pop(person, Ellipsis)
                if old_mark is not Ellipsis:
                    if old_mark is not None:
                        raise ValueError('You already checked that homework')
                    work.solutions.update({person: new_mark})
                else:
                    raise ValueError('Student never did that homework')


class Student(Person):
    def __init__(self, first_name, last_name):
        super().__init__(first_name, last_name)
        self._courses = []

    def __str__(self):
        return f"Student: {self.full_name}"

    def enroll(self, course):
        if course is not None:
            course.enroll(self)
            self._courses.append(course)

    @property
    def assigned_homeworks(self):
        homeworks = []
        for course in self._courses:
            for work in course.get_homeworks():
                if self not in work.solutions.keys():
                    homeworks.append(work)
        return homeworks

    def do_homework(self, homework):
        for course in self._courses:
            if homework in course.get_homeworks():
                homework.solutions.update({self: None})


if __name__ == '__main__':
    main_teacher = Teacher('Thomas', 'Anderson')
    assert str(main_teacher) == f'Teacher: {main_teacher.first_name} {main_teacher.last_name}'

    python_basic = Course('Python basic', '31.10.2022', 16, main_teacher)
    assert len(python_basic.lectures) == python_basic.number_of_lectures
    assert str(python_basic) == 'Python basic (31.10.2022)'
    assert python_basic.teacher == main_teacher
    assert python_basic.enrolled_by() == []
    assert main_teacher.teaching_lectures() == python_basic.lectures

    students = [Student('John', 'Doe'), Student('Jane', 'Doe')]
    for student in students:
        assert str(student) == f'Student: {student.first_name} {student.last_name}'
        student.enroll(python_basic)

    assert python_basic.enrolled_by() == students

    third_lecture = python_basic.get_lecture(3)
    assert third_lecture.name == 'Lecture 3'
    assert third_lecture.number == 3
    assert third_lecture.teacher == main_teacher
    try:
        python_basic.get_lecture(17)
    except AssertionError as error:
        assert error.args == ('Invalid lecture number',)

    third_lecture.name = 'Logic separation. Functions'
    assert third_lecture.name == 'Logic separation. Functions'

    assert python_basic.get_homeworks() == []
    assert third_lecture.get_homework() is None
    functions_homework = Homework('Functions', 'what to do here')
    assert str(functions_homework) == 'Functions: what to do here'
    third_lecture.set_homework(functions_homework)

    assert python_basic.get_homeworks() == [functions_homework]
    assert third_lecture.get_homework() == functions_homework

    for student in students:
        assert student.assigned_homeworks == [functions_homework]

    assert main_teacher.homeworks_to_check == []
    students[0].do_homework(functions_homework)
    assert students[0].assigned_homeworks == []
    assert students[1].assigned_homeworks == [functions_homework]

    assert functions_homework.done_by() == {students[0]: None}
    assert main_teacher.homeworks_to_check == [functions_homework]

    for mark in (-1, 101):
        try:
            main_teacher.check_homework(functions_homework, students[0], mark)
        except AssertionError as error:
            assert error.args == ('Invalid mark',)

    main_teacher.check_homework(functions_homework, students[0], 100)
    assert main_teacher.homeworks_to_check == []
    assert functions_homework.done_by() == {students[0]: 100}

    try:
        main_teacher.check_homework(functions_homework, students[0], 100)
    except ValueError as error:
        assert error.args == ('You already checked that homework',)

    try:
        main_teacher.check_homework(functions_homework, students[1], 100)
    except ValueError as error:
        assert error.args == ('Student never did that homework',)

    substitute_teacher = Teacher('Agent', 'Smith')
    fourth_lecture = python_basic.get_lecture(4)
    assert fourth_lecture.teacher == main_teacher

    fourth_lecture.new_teacher(substitute_teacher)
    assert fourth_lecture.teacher == substitute_teacher
    assert len(main_teacher.teaching_lectures()) == python_basic.number_of_lectures - 1
    assert substitute_teacher.teaching_lectures() == [fourth_lecture]
    assert substitute_teacher.homeworks_to_check == []

