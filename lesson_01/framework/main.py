class Framework:
    def __init__(self, routes_object):
        self.routes_list = routes_object

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        path = path if path.endswith('/') else f'{path}/'
        if path in self.routes_list:
            view = self.routes_list[path]
        else:
            view = NotFound()
        status, body = view()
        start_response(status, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]


class NotFound:
    def __call__(self):
        return '404', 'Not Found'
