from Src.Models.company_model import company_model
from Src.Core.validator import validator, argument_exception
from Src.Core.response_formats import response_formats
from datetime import datetime
from Src.Core.observe_service import observe_service
from Src.Core.event_type import event_type
from Src.Core.log_level import log_level

######################################
# Модель настроек приложения
class settings_model:
    __company: company_model = None
    __default_response_format:str = response_formats.csv()
    __block_period:datetime
    # Дата блокировки
    @property
    def block_period(self) -> datetime:
        return self.__block_period
    @block_period.setter
    def block_period(self, value:datetime):
        validator.validate(value, datetime)
        old = self.__block_period if hasattr(self, '__block_period') else None
        self.__block_period = value
        if old != value:
            # Событие: смена даты
            observe_service.create_event(event_type.change_block_period(), {'new_date': value})
            # Логирование настроек (INFO)
            observe_service.create_event(event_type.log_info(), {
                'level': log_level.INFO,
                'message': 'Block period changed',
                'context': {'old': old.strftime("%Y-%m-%d") if old else None, 'new': value.strftime("%Y-%m-%d")}
            })
            observe_service.create_event(event_type.settings_change(), {
                'level': log_level.INFO,
                'message': 'Settings updated: block_period',
                'context': {'new': value.strftime("%Y-%m-%d")}
            })

    # Текущая организация
    @property
    def company(self) -> company_model:
        return self.__company
   
    @company.setter
    def company(self, value: company_model):
        validator.validate(value, company_model)
        self.__company = value

    @property
    def default_response_format(self) -> str:
        return self.__default_response_format

    # Формат ответа по умолчанию
    @default_response_format.setter
    def default_response_format(self, value:str):
        validator.validate(value, str)
        if value not in response_formats.list_all_formats():
            raise argument_exception("Некорректно указан тип формата!")
       
        old = self.__default_response_format
        self.__default_response_format = value

        if old != value:
            observe_service.create_event(event_type.log_info(), {
                'level': log_level.INFO,
                'message': 'Default response format changed',
                'context': {'old': old, 'new': value}
            })
            observe_service.create_event(event_type.settings_change(), {
                'level': log_level.INFO,
                'message': 'Settings updated: default_response_format',
                'context': {'new': value}
            })
