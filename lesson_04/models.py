class User:
    pass


class Teacher(User):
    pass


class Student(User):
    pass


class UserFactory:
    types = {'student': Student, 'teacher': Teacher}

    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


class Course:
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)


class OnlineCourse(Course):
    def __init__(self, name, category, place):
        super().__init__(name, category)
        self.place = place


class OfflineCourse(Course):
    def __init__(self, name, category, place):
        super().__init__(name, category)
        self.place = place


class CourseFactory:
    types = {'online': OnlineCourse, 'offline': OfflineCourse}

    @classmethod
    def create(cls, type_, name, category, place):
        return cls.types[type_](name, category, place)


class Category:
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


class Model:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def get_category(self, id):
        for item in self.categories:
            if item.id == id:
                return item

    @staticmethod
    def create_course(type_, name, category, place):
        return CourseFactory.create(type_, name, category, place)

    def get_course(self, name):
        for item in self.courses:
            if item.name == name:
                return item
        return None
