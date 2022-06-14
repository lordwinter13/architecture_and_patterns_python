import sqlite3

from framework.unit_of_work import DomainObject


class User:
    def __init__(self, name):
        self.name = name


class Teacher(User):
    pass


class Student(User, DomainObject):
    def __init__(self, name):
        super().__init__(name)
        self.courses = []


class UserFactory:
    types = {'student': Student, 'teacher': Teacher}

    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


class Course:
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.students = []


    def enroll_student(self, student: Student):
        self.students.append(student)
        student.courses.append(self)

    def __getitem__(self, item):
        return self.students[item]


class OnlineCourse(Course, DomainObject):
    def __init__(self, name, category, place):
        super().__init__(name, category)
        self.place = place
        self.type_ = 'online'


class OfflineCourse(Course, DomainObject):
    def __init__(self, name, category, place):
        super().__init__(name, category)
        self.place = place
        self.type_ = 'offline'


class CourseFactory:
    types = {'online': OnlineCourse, 'offline': OfflineCourse}

    @classmethod
    def create(cls, type_, name, category, place):
        return cls.types[type_](name, category, place)


class Category(DomainObject):
    def __init__(self, name, category=None):
        self.id = category
        self.name = name
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        return result


class Model:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

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

    def get_courses(self):
        return self.courses

    def get_course(self, name):
        for item in self.courses:
            if item.name == name:
                return item
        return None

    def get_student(self, name):
        for item in self.students:
            if item.name == name:
                return item
        return None


class Mapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.table = None

    def all(self):
        statement = f"SELECT id, name from {self.table};"
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            if self.table == 'categories':
                obj = Category(name, None)
            else:
                obj = Student(name)
            obj.id = id
            result.append(obj)
        return result

    def find_by_id(self, id):
        statement = f"SELECT name, id FROM {self.table} WHERE id = ?;"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            if self.table == 'categories':
                return Category(*result)
            elif self.table == 'students':
                return Student(*result)
        else:
            raise NotFoundException(f'Id {id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.table} (name) VALUES (?);"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise CommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.table} SET name = ? WHERE id = ?;"
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise UpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.table} WHERE id = ?;"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DeleteException(e.args)


class CategoriesMapper(Mapper):
    def __init__(self, connection):
        super().__init__(connection)
        self.table = 'categories'


class StudentsMapper(Mapper):
    def __init__(self, connection):
        super().__init__(connection)
        self.table = 'students'


class CoursesMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.table = 'courses'

    def all(self):
        statement = f"SELECT id, name, category, place, type from {self.table};"
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name, category, place, type_ = item
            if type_ == 'online':
                obj = OnlineCourse(name, category, place)
            else:
                obj = OfflineCourse(name, category, place)
            obj.id = id
            obj.category = category
            obj.place = place
            obj.type_ = type_
            result.append(obj)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name, category, place, type FROM {self.table} WHERE id = ?;"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            id, name, category, place, type_ = result
            if type_ == 'online':
                return OnlineCourse(name, category, place)
            else:
                return OfflineCourse(name, category, place)
        else:
            raise NotFoundException(f'Id {id} not found')

    def find_by_parent_id(self, id):
        statement = f"SELECT id, name, category, place, type FROM {self.table} WHERE category = ?;"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchall()
        if result:
            courses = []
            for i in result:
                id, name, category, place, type_ = i
                if type_ == 'online':
                    courses.append(OnlineCourse(name, category, place))
                else:
                    courses.append(OfflineCourse(name, category, place))
            return courses

    def insert(self, obj):
        statement = f"INSERT INTO {self.table} (name, category, place, type) VALUES (?, ?, ?, ?);"
        self.cursor.execute(statement, (obj.name, obj.category.id, obj.place, obj.type_))
        try:
            self.connection.commit()
        except Exception as e:
            raise CommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.table} SET name = ?, category = ?, place = ?, type = ? WHERE id = ?;"
        self.cursor.execute(statement, (obj.name, obj.id, obj.category.id, obj.place, obj.type_))
        try:
            self.connection.commit()
        except Exception as e:
            raise UpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.table} WHERE id = ?;"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DeleteException(e.args)


connection = sqlite3.connect('database.sqlite')


class MapperRegistry:
    mappers = {
        'student': StudentsMapper,
        'category': CategoriesMapper,
        'course': CoursesMapper
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Student):
            return StudentsMapper(connection)
        elif isinstance(obj, Category):
            return CategoriesMapper(connection)
        elif isinstance(obj, Course):
            return CoursesMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)


class CommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Commit error: {message}')


class UpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Update error: {message}')


class DeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Delete error: {message}')


class NotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Data not found: {message}')
