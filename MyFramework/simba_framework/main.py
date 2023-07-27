from typing import Callable
from .framework_requests import GetRequest, PostRequest
import quopri


class PageNotFound404:
    def __call__(self, request):
        return "404 WHAT ", "404 PAGE Not Found"

#Класс Framework - основа WSGI фреймворка
class Framework:

    def decode_value(self, data):
        new_data = {}
        for key, value in data.items():
            value = bytes(value.replace("%", "=").replace("+", ""), 'UTF-8')
            value_decode_str = quopri.decodestring(value).decode("utf-8")
            new_data[key] = value_decode_str
        return new_data
    def __init__(self, routes_obj):
        #router_lst - словарь привязок
        self.routes_lst = routes_obj

    def GET_req(self, request: dict, environ: dict) -> None:
        GET_params = environ["QUERY_STRING"]
        request_params = GetRequest().get_request_params(GET_params)
        request['request_params'] = request_params
        print(f"К нам пришли GET параметры - {request_params}")

    def POST_req(self, request: dict, environ: dict) -> None:
        data = PostRequest().get_request_params(environ)
        request["data"] = data
        print(f"К нам пришел POST запрос - {self.decode_value(data)}")

    def get_request(self, environ: dict) -> dict:
        request = {}
        method = environ["REQUEST_METHOD"]
        request["method"] = method
        if method == "GET":
            self.GET_req(request, environ)
        if method == "POST":
            self.POST_req(request, environ)
        return request

    #Точка входа
    def __call__(self, environ: dict, start_responce: Callable):
        #Получаем адрес, по которому пользователь выполнил переход
        path: str = environ.get("PATH_INFO")

        if not path.endswith("/"):
            path = f"{path}/"
        request = self.get_request(environ)

        #Находим нужный контроллер
        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = PageNotFound404()


        #Получаем данные запроса
        code, body = view(request)

        # request = {}
        # method = environ["REQUEST_METHOD"]
        # request["method"] = method
        # if method == "GET":
        #     GET_params = environ["QUERY_STRING"]
        #     request_params = GetRequest().get_request_params(GET_params)
        #     request['request_params'] = request_params
        #     print(f"К нам пришли GET параметры - {request_params}")

        #Запускаем контроллер


        #Для заголовков
        start_responce(code, [("Content-Type", "text/html")])

        #Наше тело запроса
        return [body.encode("utf-8")]
