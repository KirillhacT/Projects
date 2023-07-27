from jinja2 import FileSystemLoader
from jinja2.environment import Environment

def render(template_name: str, folder: str = "templates", **kwargs) -> str:
    """
    :param template_name: имя шаблона
    :param folder: папка, в которой ищем шаблон
    :param kwargs: параметры, передаваемые в шаблон
    :return:
    """
    env = Environment()
    env.loader = FileSystemLoader(folder)
    template = env.get_template(template_name)
    return template.render(**kwargs)

    #Улучшаем старый код при помощи шаблонизатора jinja
    # file_path = join(folder, template_name)
    # #Открываем шаблон по имени
    # with open(file_path, "r", encoding="utf-8") as file:
    #     #Читаем
    #     template = Template(file.read())
    # # Рендерим шаблон с параметрами
    # return template.render(**kwargs)


