import json
from keyword import iskeyword  # для проверки, что строка является ключевым словом


class TransformJSON:
    """Класс для преобразования JSON-объеĸтов в python-объеĸты
        с доступом к атрибутам через точĸу """

    def __init__(self, dictionary, is_parent_instance=1):
        for keys in dictionary:
            value = dictionary[keys]
            if isinstance(value, dict):
                is_parent_instance = 0
                value = Advert(value)
            setattr(self, keys, value)
        if is_parent_instance == 0:
            if hasattr(self, 'price'):
                if self.price < 0:
                    raise ValueError('price must be >= 0')
            else:
                self.price = 0


class ColorMixin:
    """Класс для изменения цвета теĸста при выводе на ĸонсоль"""
    repr_color_code = 33

    def __str__(self):
        return f"\033[1;{self.repr_color_code};10m {self.__repr__()} \n"


class Advert(TransformJSON, ColorMixin):
    repr_color_code = 33

    def __init__(self, dictionary):
        super().__init__(dictionary, is_parent_instance=1)
        to_change = []
        for attr in self.__dict__:
            if iskeyword(attr):
                to_change.append(attr)
        for attr in to_change:
            self.__dict__[attr + '_'] = self.__dict__.pop(attr)

    def __repr__(self):
        return f'{self.title} | {self.price} ₽'


if __name__ == '__main__':
    # создаем экземпляр класса Advert из JSON
    lesson_str = """{
"title": "python",
"price": 1,
"location": {
"address": "город Москва, Лесная, 7",
"metro_stations": ["Белорусская"]
}
}"""

    lesson = json.loads(lesson_str)
    lesson_ad = Advert(lesson)
    print('lesson_ad:', lesson_ad)
    print('lesson_ad.location.address:', lesson_ad.location.address)

    lesson_str2 = """{"title": "Вельш-корги",
                "class": "dogs",
                "location": {
                "address": "сельское поселение Ельдигинское, поселок санатория Тишково, 25"
                            }
                    }"""
    lesson2 = json.loads(lesson_str2)
    lesson_ad2 = Advert(lesson2)
    print('lesson_ad2 без цены:', lesson_ad2)
    print('lesson_ad2.class_:', lesson_ad2.class_)

    lesson_str3 = """{ "title": "python",
                        "price": -1,
                        "location": {
                            "address": "город Москва, Лесная, 7",
                            "metro_stations": ["Белорусская"]
                                    }
}"""
    lesson3 = json.loads(lesson_str3)
    lesson_ad3 = Advert(lesson3)
    print('lesson_ad3 c отрицательной ценой:', lesson_ad3)
