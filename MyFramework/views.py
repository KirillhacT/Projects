import datetime

from simba_framework.templator import render
from components.models import Engine
from components.decorators import AppRoute
from components.cbv import ListView, CreateView

site = Engine()
routes = {}
@AppRoute(routes=routes, url="/")
class Index(ListView):
    # def __call__(self, request: dict):
    #     return "200 OK", render('index.html', objects_list=site.categories)
    template_name = "index.html"
    queryset = site.categories
    context_object_name = "category_list"

@AppRoute(routes=routes, url="/about/")
class About:
    def __call__(self, request: dict):
        return "200 OK", render("about.html")


@AppRoute(routes=routes, url="/study_programs/")
class StudyPrograms:
    def __call__(self, request: dict):
        return "200 OK", render("study-programs.html", date=datetime.date.today())

@AppRoute(routes=routes, url="/post-list/")
class Post(ListView):
    template_name = "post-list.html"
    queryset = site.posts
    context_object_name = "post_list"
    # def get_queryset(self):
    #     return site.posts

    # def get_context_data(self):
    #     #Возвращает context, который уже был получен в методе, переопределеннои из класса TemplateName
    #     context = super().get_context_data()
    #     context["lal"] = "kek"
    #     return context

@AppRoute(routes=routes, url="/post-create/")
class GetPost(CreateView):
    template_name = "post-create.html"

    def create_obj(self, data):
        title = site.decode_value(data["title"])
        description = site.decode_value(data["description"])
        post = site.create_post(title, description)
        site.posts.append(post)

    # def get_context_data(self):
    #     context = super().get_context_data()
    #     context["lal"] = "kek"
    #     return context


class NotFound404:
    def __call__(self, request: dict):
        return "404 WHAT", "404 PAGE NOT FOUND"

@AppRoute(routes=routes, url="/create-category/")
class CreateCategory(CreateView):
    template_name = "create_category.html"
    def create_obj(self, data):
        name = data["name"]
        name = site.decode_value(name)
        category_id = data.get('category_id')
        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))
        new_category = site.create_category(name, category)  # !!!
        site.categories.append(new_category)

    # def __call__(self, request):
    #     if request["method"] == "POST":
    #         data = request['data']
    #         name = data["name"]
    #         name = site.decode_value(name)
    #         category_id = data.get('category_id')
    #
    #         category = None
    #         if category_id:
    #             category = site.find_category_by_id(int(category_id))
    #         new_category = site.create_category(name, category) #!!!
    #         site.categories.append(new_category)
    #         print(new_category)
    #         return "200 OK", render('index.html', category_list=site.categories)
    #     else:
    #         categories = site.categories
    #         return "200 OK", render('create_category.html', categories=categories)


# @AppRoute(routes=routes, url="/courses-list/")
# class Course_list:
#     """Находит в памяти нужную категорию по id из get запроса
#     и отправляет в шаблон курсы, относящиеся к категории, имя
#     категории и ее id
#     """
#     def __call__(self, request: dict):
#         try:
#             category = site.find_category_by_id(
#                 int(request.get('request_params')["id"])
#             )
#             return '200 OK', render('course_list.html',
#                                     objects_list=category.courses,
#                                     name=category.name,
#                                     id=category.id)
#         except KeyError:
#             return '200 OK', 'No courses have been added yet'

#!
# @AppRoute(routes=routes, url="/create-course/")
# class Create_course:
#     """Cоздает новый курс"""
#     category_id = -1
#
#     def __call__(self, request: dict):
#         if request["method"] == 'POST':
#             data = request.get("data")
#             name = data["name"]
#             name = site.decode_value(name)
#
#             category = None
#             if self.category_id != -1:
#                 category = site.find_category_by_id(int(self.category_id))
#                 course = site.create_course('record', name, category)
#                 site.courses.append(course)
#             return '200 OK', render('course_list.html', objects_list=category.courses,
#                                     name=name,
#                                     id=category.id)
#         else:
#             try:
#                 self.category_id = int(request["request_params"]["id"])
#                 print(f"axx {request}")
#                 category = site.find_category_by_id(int(self.category_id))
#                 return "200 OK", render('create_course.html',
#                                         name=category.name,
#                                         id=category.id)
#             except KeyError:
#                 return "200 OK", "No categories"

