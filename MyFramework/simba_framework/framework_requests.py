#Обработка Get запроса
#Пример:
#http://127.0.0.1:8080/?id=1&target=hello

class ParserMixin:
    def _parse_input_data(self, data: str) -> dict:
        result = {}
        if data:
            params = data.split("&")
            for item in params:
                key, value = item.split("=")
                result[key] = value
            return result
        #{
        #   id: 1,
        #   target: "hello",
        #}


class GetRequest(ParserMixin):

    def get_request_params(self, GET_data: str) -> dict:
        #Получаем параметры запроса типа
        #id=1&target=hello
        request_params = self._parse_input_data(GET_data)
        return request_params


class PostRequest(ParserMixin):
    # def _parse_input_data(self, data: str):
    #     return self._parse_data(data)

    @staticmethod
    def _get_wsgi_input_data(environ: dict) -> bytes:
        #Получаем длину тела
        content_lenght_data = environ.get("CONTENT_LENGTH")
        #Приводим к int
        content_lenght = int(content_lenght_data) if content_lenght_data else 0
        #Считываем данные, если они есть
        data = environ['wsgi.input'].read(content_lenght) if content_lenght > 0 else b''
        return data

    def _parse_wsgi_input_data(self, data: bytes) -> dict:
        result = {}
        if data:
            # print(data)
            data_str = data.decode(encoding="utf-8")
            # print(data_str)
            result = self._parse_input_data(data_str)
            # print(result)
        return result

    def get_request_params(self, environ) -> dict:
        #Получаем данные
        data_bytes = self._get_wsgi_input_data(environ) #САМЫЙ ВАЖНЫЙ МЕТОД
        #Превращаем данные в словарь
        data_dict = self._parse_wsgi_input_data(data_bytes)
        return data_dict





