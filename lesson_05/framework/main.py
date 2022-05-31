import views
import quopri

from framework.requests import GetRequest, PostRequest
from framework.decorators import Route


class Framework:
    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        path = path if path.endswith('/') else f'{path}/'

        request = {}
        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'GET':
            request_params = GetRequest.get_params(environ)
            request['request_params'] = request_params
            print(f'Получен GET-запрос: {request_params}')

        if method == 'POST':
            data = PostRequest.get_params(environ)
            data = Framework.decode_data(data)
            request['data'] = data
            print(f'Получен POST-запрос: {data}')

        routes_list = Route.get_routes()
        if path in routes_list:
            view = routes_list[path]
        else:
            view = routes_list['/404/']
        status, body = view(request)
        start_response(status, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_data(data: dict) -> dict:
        decoded_data = {}
        for key, value in data.items():
            tmp_value = bytes(value.replace('%', '=').replace('+', ' '), 'UTF-8')
            tmp_value = quopri.decodestring(tmp_value).decode('UTF-8')
            decoded_data[key] = tmp_value
        return decoded_data
