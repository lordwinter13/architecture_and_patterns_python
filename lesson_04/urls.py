from views import Index, About, Contacts, NotFound, Categories, NewCategory, Courses, NewCourse

routes = {
    '/': Index(),
    '/about/': About(),
    '/contacts/': Contacts(),
    '/404/': NotFound(),
    '/categories/': Categories(),
    '/new-category/': NewCategory(),
    '/courses/': Courses(),
    '/new-course/': NewCourse()
}
