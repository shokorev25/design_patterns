from Src.reposity_manager import reposity_manager
from Src.Models.settings_model import settings_model
from Src.settings_manager import settings_manager
from datetime import datetime
from Src.Core.prototype import prototype
from Src.Core.abstract_logic import abstract_logic
from Src.Core.observe_service import observe_service
from Src.Core.event_type import event_type
from Src.Models.rest_model import rest_model
from collections import defaultdict

# Сервис для расчета остатков
class rest_service(abstract_logic):
    # Репозиторий
    __repo: reposity_manager = reposity_manager()

    # Текущие настройки
    __settings:settings_model = settings_manager().settings

    # Рассчитать остатки
    def __init__(self):
        super().__init__()
        observe_service.add(self)

    def handle(self, event: str, params):
        super().handle(event, params)
        if event == event_type.change_block_period():
            self.calc()

    def calc(self) -> list:
        rests = []
        block_date = self.__settings.block_period
        trans_dict = defaultdict(float)
        transactions = self.__repo.data[reposity_manager.transaction_key()]
        for trans in transactions:
            if trans.period <= block_date:
                key = (trans.storage.unique_code, trans.nomenclature.unique_code, trans.range.unique_code)
                trans_dict[key] += trans.value

        for key, value in trans_dict.items():
            if value != 0:
                storage_id, nom_id, range_id = key
                rest = rest_model()
                rest.storage = [s for s in self.__repo.data[reposity_manager.storage_key()] if s.unique_code == storage_id][0]
                rest.nomenclature = [n for n in self.__repo.data[reposity_manager.nomenclature_key()] if n.unique_code == nom_id][0]
                rest.range = [r for r in self.__repo.data[reposity_manager.range_key()] if r.unique_code == range_id][0]
                rest.value = value
                rests.append(rest)

        self.__repo.data[reposity_manager.rest_key()] = rests
        self.__repo.save()
        return rests