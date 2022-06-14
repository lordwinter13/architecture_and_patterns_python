class Route:
    routes = {}

    def __init__(self, url):
        self.url = url

    def __call__(self, view):
        Route.routes[self.url] = view()

    @staticmethod
    def get_routes():
        return Route.routes
