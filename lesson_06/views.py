from framework.templator import render
from framework.decorators import Route
from models import Model

site = Model()


@Route('/')
class Index:
    def __call__(self, request):
        return '200 OK', render('index.html')


@Route('/about/')
class About:
    def __call__(self, request):
        return '200 OK', render('about.html')


@Route('/contacts/')
class Contacts:
    def __call__(self, request):
        return '200 OK', render('contacts.html')


@Route('/404/')
class NotFound:
    def __call__(self, request):
        return '200 OK', render('404.html')


@Route('/categories/')
class Categories:
    def __call__(self, request):
        return '200 OK', render('categories.html', categories_list=site.categories)


@Route('/new-category/')
class NewCategory:
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            new_category = site.create_category(name)
            site.categories.append(new_category)
            return '200 OK', render('categories.html', categories_list=site.categories)
        else:
            return '200 OK', render('new-category.html', categories_list=site.categories)


@Route('/api/')
class ApiCourses:
    def __call__(self, request):
        courses = site.get_courses()
        result = {
            'courses': [
                {
                    'name': i.name,
                    'category': i.category.name,
                    'place': i.place
                } for i in courses
            ]
        }
        return '200 OK', result


@Route('/courses/')
class Courses:
    def __call__(self, request):
        try:
            category = site.get_category(int(request['request_params']['id'][0]))
            if not category:
                raise KeyError
            return '200 OK', render(
                'courses.html',
                courses_list=category.courses,
                category_name=category.name,
                id=category.id
            )
        except KeyError:
            return '200 OK', render('404.html')


@Route('/new-course/')
class NewCourse:
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            course_type = data['type']
            place = data['place']
            category = site.get_category(int(self.category_id))
            course = site.create_course(course_type, name, category, place)
            site.courses.append(course)
            return '200 OK', render(
                'courses.html',
                courses_list=category.courses,
                category_name=category.name,
                id=category.id
            )
        else:
            try:
                self.category_id = int(request['request_params']['id'][0])
                category = site.get_category(int(self.category_id))
                if not category:
                    raise KeyError
                return '200 OK', render('new-course.html', category_name=category.name, id=category.id)
            except KeyError:
                return '200 OK', render('404.html')


@Route('/students/')
class Students:
    def __call__(self, request):
        return '200 OK', render('students.html', students_list=site.students)


@Route('/new-student/')
class NewStudent:
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            new_student = site.create_user('student', name)
            site.students.append(new_student)
            return '200 OK', render('students.html', students_list=site.students)
        else:
            return '200 OK', render('new-student.html')


@Route('/enroll-student/')
class EnrollStudent:
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            course = data['course']
            course = site.get_course(course)
            student = data['student']
            student = site.get_student(student)
            course.enroll_student(student)
            return '200 OK', render('students.html', students_list=site.students)
        else:
            return '200 OK', render('enroll-student.html', students_list=site.students, courses_list=site.courses)
