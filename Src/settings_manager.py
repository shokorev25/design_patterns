from Src.Models.settings_model import settings_model
from Src.Core.validator import operation_exception
from Src.Core.validator import validator
from Src.Models.company_model import company_model
from Src.Core.common import common
from Src.Core.response_formats import response_formats
import json
from datetime import datetime
from Src.Core.abstract_manager import abstract_manager
from Src.Logics.convert_factory import convert_factory
from Src.Core.observe_service import observe_service
from Src.Core.event_type import event_type
from Src.Core.log_level import log_level

####################################################3
# Менеджер настроек.
# Предназначен для управления настройками и хранения параметров приложения
class settings_manager(abstract_manager):

    # Настройки
    __settings:settings_model = None

    # Singletone
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(settings_manager, cls).__new__(cls)
        return cls.instance
   
    def __init__(self):
        self.__set_default()

    # Текущие настройки
    @property
    def settings(self) -> settings_model:
        return self.__settings

    # Загрузить настройки из Json файла
    def load(self) -> bool:
        if self.file_name == "":
            raise operation_exception("Не найден файл настроек!")

        try:
            with open( self.file_name, 'r', encoding='utf-8') as file_instance:
                settings = json.load(file_instance)

                # Реквизиты оргаизации
                result = True
                if "company" in settings.keys():
                    data = settings["company"]
                    result = self.__deserialize(data)
               
                # Формат по умолчанию
                if "default_format" in settings.keys() and result == True:
                    data = settings["default_format"]
                    if data in response_formats.list_all_formats():
                        self.settings.default_response_format = data

                # Дата блокировки
                if "block_period" in settings.keys() and result == True:
                    data = settings["block_period"]
                    date_format = "%Y-%m-%d"
                    date = datetime.strptime(data, date_format)
                    self.__settings.block_period = date

                if "logging" in settings.keys():
                    logging = settings["logging"]
                    observe_service.create_event(event_type.settings_change(), {
                        'level': log_level.INFO,
                        'message': 'Logging settings loaded',
                        'context': {
                            'min_level': logging.get('min_level'),
                            'output': logging.get('output'),
                            'file_name': logging.get('file_name')
                        }
                    })

                observe_service.create_event(event_type.log_info(), {
                    'level': log_level.INFO,
                    'message': 'Settings loaded successfully',
                    'context': {'file': self.file_name}
                })
                return result
            return False
        except Exception as ex:
            observe_service.create_event(event_type.log_error(), {
                'level': log_level.ERROR,
                'message': 'Settings load failed',
                'context': {'file': self.file_name, 'error': str(ex)}
            })
            return False
       
    # Обработать полученный словарь
    def __deserialize(self, data: dict) -> bool:
        validator.validate(data, dict)

        fields = common.get_fields(self.__settings.company)
        matching_keys = list(filter(lambda key: key in fields, data.keys()))

        try:
            for key in matching_keys:
                setattr(self.__settings.company, key, data[key])
        except:
            return False
        return True

    # Параметры настроек по умолчанию
    def __set_default(self):
        company = company_model()
        company.name = "Рога и копыта"
        company.inn = -1
       
        self.__settings = settings_model()
        self.__settings.company = company

    def save(self) -> bool:
        if self.file_name == "":
            raise operation_exception("No settings file specified!")
        data = {}
        factory = convert_factory()
        data['company'] = factory.serialize(self.settings.company)
        data['default_format'] = self.settings.default_response_format
        data['block_period'] = self.settings.block_period.strftime("%Y-%m-%d")
        try:
            with open(self.file_name, 'r', encoding='utf-8') as f:
                existing = json.load(f)
        except:
            existing = {}
        if 'logging' in existing:
            data['logging'] = existing['logging']

        try:
            with open(self.file_name, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            observe_service.create_event(event_type.log_info(), {
                'level': log_level.INFO,
                'message': 'Settings saved successfully',
                'context': {'file': self.file_name}
            })
            return True
        except Exception as ex:
            observe_service.create_event(event_type.log_error(), {
                'level': log_level.ERROR,
                'message': 'Settings save failed',
                'context': {'file': self.file_name, 'error': str(ex)}
            })
            return False
