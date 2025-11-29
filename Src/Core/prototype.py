from Src.Core.validator import validator
from Src.Dtos.filter_dto import filter_dto
from Src.Core.common import common
from Src.Core.condition_type import condition_type

# Абстрактный класс - прототип
class prototype:
    __data = []

    # Набор данных
    @property
    def data(self):
        return self.__data

    def __init__(self, data:list):
        validator.validate(data, list)
        self.__data = data

    # Клонирование
    def clone(self, data:list = None)-> "prototype":
        inner_data = None
        if data is None:
            inner_data = self.__data
        else:
            inner_data = data
        instance = prototype(inner_data)
        return instance
   
    # Универсальный фильтр
    @staticmethod
    def filter(data:list, filter:filter_dto ) -> list:
        if len(data) == 0:
            return data
       
        result = []
        for item in data:
            try:
                value = nested_getattr(item, filter.field_name)
                str_value = str(value)
                if filter.condition == condition_type.EQUALS:
                    if str_value == filter.value:
                        result.append(item)
            except AttributeError:
                pass
        return result
               
def nested_getattr(obj, attr_str):
    attrs = attr_str.split('.')
    current = obj
    for attr in attrs:
        current = getattr(current, attr)
    return current