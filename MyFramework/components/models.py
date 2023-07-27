import quopri
from typing import Union


class PostMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = "posts"

    def all(self):
        statement = f"SELECT * from {self.tablename}"
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            title, description = item
            post = Post(title, description)
            result.append(post)
        return result

    def find_by_title(self, title):
        statement = f"SELECT title, description FROM {self.tablename} WHERE title={title}"
        self.cursor.execute(statement)
        result = self.cursor.fetchone()
        if result:
            return Post(*result)
        else:
            raise Exception("Page not found")

    def insert(self, obj):
        statement = f"UPDATE {self.tablename} SET description={obj.description} WHERE title={obj.title}"
        try:
            self.connection.commit()
        except Exception as ex:
            print(ex)
class Post:
    def __init__(self, title, description):
        self.title = title
        self.description = description

class PostFactory:
    types = {
        "post": Post
    }
    @classmethod
    def create(cls, type_, title, description):
        return cls.types[type_](title, description)


class Category:
    auto_id = 0
    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category

class Engine:
    def __init__(self):
        self.courses = []
        self.categories = []
        self.posts = []

    @staticmethod
    def create_post(title, description) -> Post:
        post = PostFactory.create("post", title, description)
        return post

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace('+', ' '), 'UTF-8')
        val_decode_str = quopri.decodestring(val_b)
        return val_decode_str.decode("utf-8")

    @staticmethod
    def create_category(name, category=None) -> Category:
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            print("item", item.id)
            if item.id == id:
                return item
        raise Exception(f"Нет категории с id = {id}")


