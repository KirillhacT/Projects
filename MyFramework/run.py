from wsgiref.simple_server import make_server
from simba_framework.main import Framework
# from urls import routes
from views import routes

#Создаем объект WSGI-приложения
application = Framework(routes)

with make_server('', 8080, application) as httpd:
    print("Запуск по адресу http://127.0.0.1:8080/...")
    httpd.serve_forever()