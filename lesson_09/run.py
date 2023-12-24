# from framework.main import Framework
#
# app = Framework()


from wsgiref.simple_server import make_server
from framework.main import Framework

app = Framework()

with make_server('', 8080, app) as httpd:
    print("Запуск на порту 8080...")
    httpd.serve_forever()
