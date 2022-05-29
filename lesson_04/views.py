from framework.templator import render
from models import Model

site = Model()


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html')


class About:
    def __call__(self, request):
        return '200 OK', render('about.html')


class Contacts:
    def __call__(self, request):
        return '200 OK', render('contacts.html')


class NotFound:
    def __call__(self, request):
        return '200 OK', render('404.html')


class Categories:
    def __call__(self, request):
        return '200 OK', render('categories.html', categories_list=site.categories)


class NewCategory:
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            new_category = site.create_category(name)
            site.categories.append(new_category)
            return '200 OK', render('categories.html', categories_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('new-category.html', categories_list=categories)


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
