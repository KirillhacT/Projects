from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, \
    InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

start_kb = ReplyKeyboardMarkup(resize_keyboard=True)
start_b1 = KeyboardButton("Меню")
start_b2 = KeyboardButton("Помощь")
start_kb.add(start_b1)
start_kb.insert(start_b2)

ikb = InlineKeyboardMarkup(row_width=2)
ib1 = InlineKeyboardButton(text='❤️', callback_data="like")
ib2 = InlineKeyboardButton(text='👎', callback_data="dislike")
ib3 = InlineKeyboardButton(text='Следующее фото', callback_data="dont_like")
ib4= InlineKeyboardButton(text='Главное меню', callback_data="menu")
ikb.add(ib1, ib2).add(ib3).add(ib4)

cb = CallbackData("ikb", "action")

def get_inline_keyboard() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Прибавить", callback_data=cb.new('btn_+')), InlineKeyboardButton("Убавить", callback_data=cb.new("btn_-"))],
        [InlineKeyboardButton("Рандомное число", callback_data=cb.new("btn_random"))]
    ])
    return ikb

class ExitReplay:
    def __init__(self, *params, exit=True):
        self.kb = ReplyKeyboardMarkup(resize_keyboard=True)
        if exit:
            self.kb.add(KeyboardButton("Выход"))
        count = 2
        for _param in params:
            ind = count % 2 == 0
            self.params_add(_param, ind)
            count += 1
    def __call__(self, *args, **kwargs):
        return self.kb

    def params_add(self, _param, ind):
        k_i = KeyboardButton(_param)
        if ind:
            self.kb.add(k_i)
        else:
            self.kb.insert(k_i)

menu_kb = ExitReplay('Помощь', 'Отправить фото', 'Счетчик', "Задать вопрос", "Создание профиля", exit=False)()
# b1 = KeyboardButton('help')
# b2 = KeyboardButton('/echo')
# b3 = KeyboardButton('send_photo')
# kb.add(b1, b2, b3, b4)
