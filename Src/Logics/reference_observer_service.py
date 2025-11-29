from Src.Core.abstract_logic import abstract_logic
from Src.Core.observe_service import observe_service
from Src.Core.event_type import event_type
from Src.Core.validator import operation_exception
from Src.reposity_manager import reposity_manager
from Src.Core.prototype import prototype
from Src.Dtos.filter_dto import filter_dto
from Src.Core.condition_type import condition_type

class reference_observer_service(abstract_logic):
    __repo = reposity_manager()

    def __init__(self):
        super().__init__()
        observe_service.add(self)

    def handle(self, event: str, params):
        super().handle(event, params)
        if event == event_type.delete_group():
            self._check_delete_group(params['group'])
        elif event == event_type.delete_range():
            self._check_delete_range(params['range'])
        elif event == event_type.delete_nomenclature():
            self._check_delete_nomenclature(params['nomenclature'])
        elif event == event_type.delete_storage():
            self._check_delete_storage(params['storage'])

    def _check_delete_group(self, group):
        noms = self.__repo.data[reposity_manager.nomenclature_key()]
        filter_ = filter_dto.create_equals_filter('group.unique_code', group.unique_code)
        used = prototype.filter(noms, filter_)
        if len(used) > 0:
            raise operation_exception("Cannot delete group, used in nomenclatures")

    def _check_delete_range(self, range_):
        noms = self.__repo.data[reposity_manager.nomenclature_key()]
        filter_ = filter_dto.create_equals_filter('range.unique_code', range_.unique_code)
        used_nom = prototype.filter(noms, filter_)
        if len(used_nom) > 0:
            raise operation_exception("Cannot delete range, used in nomenclatures")

        trans = self.__repo.data[reposity_manager.transaction_key()]
        used_trans = prototype.filter(trans, filter_)
        if len(used_trans) > 0:
            raise operation_exception("Cannot delete range, used in transactions")

        if self._is_used_in_receipts(range_, 'range'):
            raise operation_exception("Cannot delete range, used in receipts")

    def _check_delete_nomenclature(self, nom):
        trans = self.__repo.data[reposity_manager.transaction_key()]
        filter_ = filter_dto.create_equals_filter('nomenclature.unique_code', nom.unique_code)
        used_trans = prototype.filter(trans, filter_)
        if len(used_trans) > 0:
            raise operation_exception("Cannot delete nomenclature, used in transactions")

        if self._is_used_in_receipts(nom, 'nomenclature'):
            raise operation_exception("Cannot delete nomenclature, used in receipts")

    def _check_delete_storage(self, storage):
        trans = self.__repo.data[reposity_manager.transaction_key()]
        filter_ = filter_dto.create_equals_filter('storage.unique_code', storage.unique_code)
        used = prototype.filter(trans, filter_)
        if len(used) > 0:
            raise operation_exception("Cannot delete storage, used in transactions")

    def _is_used_in_receipts(self, obj, type_):
        receipts = self.__repo.data[reposity_manager.receipt_key()]
        for receipt in receipts:
            for item in receipt.composition:
                if type_ == 'range' and item.range == obj:
                    return True
                elif type_ == 'nomenclature' and item.nomenclature == obj:
                    return True
        return False