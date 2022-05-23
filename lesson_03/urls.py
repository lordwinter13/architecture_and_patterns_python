from views import Index, About, Contacts, NotFound

routes = {
    '/': Index(),
    '/about/': About(),
    '/contacts/': Contacts(),
    '/404/': NotFound()
}
