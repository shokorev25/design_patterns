from Src.reposity_manager import reposity_manager
from Src.Core.abstract_logic import abstract_logic
from Src.Core.validator import validator, operation_exception
from Src.Core.prototype import prototype
from Src.Dtos.filter_dto import filter_dto
from Src.Core.condition_type import condition_type
from Src.Models.group_model import group_model
from Src.Models.range_model import range_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.storage_model import storage_model
from Src.Dtos.category_dto import category_dto
from Src.Dtos.range_dto import range_dto
from Src.Dtos.nomenclature_dto import nomenclature_dto
from Src.Dtos.storage_dto import storage_dto
from Src.Core.observe_service import observe_service
from Src.Core.event_type import event_type

class reference_service(abstract_logic):
    __repo = reposity_manager()

    def __get_cache(self):
        cache = {}
        keys = self.__repo.keys()
        for key in keys:
            for item in self.__repo.data[key]:
                cache[item.unique_code] = item
        return cache

    def add_group(self, group: group_model):
        validator.validate(group, group_model)
        self.__repo.data[reposity_manager.group_key()].append(group)
        self.__repo.save()

    def update_group(self, group_id: str, updated_group: group_model):
        validator.validate(group_id, str)
        validator.validate(updated_group, group_model)
        groups = prototype(self.__repo.data[reposity_manager.group_key()])
        filter_ = filter_dto.create_equals_filter('unique_code', group_id)
        found = groups.filter(groups.data, filter_)
        if not found:
            raise operation_exception("Group not found")
        old_group = found[0]
        old_group.name = updated_group.name
        self.__repo.save()

    def delete_group(self, group_id: str):
        validator.validate(group_id, str)
        groups = prototype(self.__repo.data[reposity_manager.group_key()])
        filter_ = filter_dto.create_equals_filter('unique_code', group_id)
        found = groups.filter(groups.data, filter_)
        if not found:
            raise operation_exception("Group not found")
        group = found[0]
        observe_service.create_event(event_type.delete_group(), {'group': group})
        self.__repo.data[reposity_manager.group_key()].remove(group)
        self.__repo.save()

    def get_group(self, group_id: str) -> group_model:
        validator.validate(group_id, str)
        groups = prototype(self.__repo.data[reposity_manager.group_key()])
        filter_ = filter_dto.create_equals_filter('unique_code', group_id)
        found = groups.filter(groups.data, filter_)
        if not found:
            return None
        return found[0]

    def add_range(self, range_: range_model):
        validator.validate(range_, range_model)
        self.__repo.data[reposity_manager.range_key()].append(range_)
        self.__repo.save()

    def update_range(self, range_id: str, updated_range: range_model):
        validator.validate(range_id, str)
        validator.validate(updated_range, range_model)
        ranges = prototype(self.__repo.data[reposity_manager.range_key()])
        filter_ = filter_dto.create_equals_filter('unique_code', range_id)
        found = ranges.filter(ranges.data, filter_)
        if not found:
            raise operation_exception("Range not found")
        old_range = found[0]
        old_range.name = updated_range.name
        old_range.value = updated_range.value
        old_range.base = updated_range.base
        self.__repo.save()

    def delete_range(self, range_id: str):
        validator.validate(range_id, str)
        ranges = prototype(self.__repo.data[reposity_manager.range_key()])
        filter_ = filter_dto.create_equals_filter('unique_code', range_id)
        found = ranges.filter(ranges.data, filter_)
        if not found:
            raise operation_exception("Range not found")
        range_ = found[0]
        observe_service.create_event(event_type.delete_range(), {'range': range_})
        self.__repo.data[reposity_manager.range_key()].remove(range_)
        self.__repo.save()

    def get_range(self, range_id: str) -> range_model:
        validator.validate(range_id, str)
        ranges = prototype(self.__repo.data[reposity_manager.range_key()])
        filter_ = filter_dto.create_equals_filter('unique_code', range_id)
        found = ranges.filter(ranges.data, filter_)
        if not found:
            return None
        return found[0]

    def add_nomenclature(self, nom: nomenclature_model):
        validator.validate(nom, nomenclature_model)
        self.__repo.data[reposity_manager.nomenclature_key()].append(nom)
        self.__repo.save()

    def update_nomenclature(self, nom_id: str, updated_nom: nomenclature_model):
        validator.validate(nom_id, str)
        validator.validate(updated_nom, nomenclature_model)
        noms = prototype(self.__repo.data[reposity_manager.nomenclature_key()])
        filter_ = filter_dto.create_equals_filter('unique_code', nom_id)
        found = noms.filter(noms.data, filter_)
        if not found:
            raise operation_exception("Nomenclature not found")
        old_nom = found[0]
        old_nom.name = updated_nom.name
        old_nom.group = updated_nom.group
        old_nom.range = updated_nom.range
        self.__repo.save()

    def delete_nomenclature(self, nom_id: str):
        validator.validate(nom_id, str)
        noms = prototype(self.__repo.data[reposity_manager.nomenclature_key()])
        filter_ = filter_dto.create_equals_filter('unique_code', nom_id)
        found = noms.filter(noms.data, filter_)
        if not found:
            raise operation_exception("Nomenclature not found")
        nom = found[0]
        observe_service.create_event(event_type.delete_nomenclature(), {'nomenclature': nom})
        self.__repo.data[reposity_manager.nomenclature_key()].remove(nom)
        self.__repo.save()

    def get_nomenclature(self, nom_id: str) -> nomenclature_model:
        validator.validate(nom_id, str)
        noms = prototype(self.__repo.data[reposity_manager.nomenclature_key()])
        filter_ = filter_dto.create_equals_filter('unique_code', nom_id)
        found = noms.filter(noms.data, filter_)
        if not found:
            return None
        return found[0]

    # Storage operations
    def add_storage(self, storage: storage_model):
        validator.validate(storage, storage_model)
        self.__repo.data[reposity_manager.storage_key()].append(storage)
        self.__repo.save()

    def update_storage(self, storage_id: str, updated_storage: storage_model):
        validator.validate(storage_id, str)
        validator.validate(updated_storage, storage_model)
        storages = prototype(self.__repo.data[reposity_manager.storage_key()])
        filter_ = filter_dto.create_equals_filter('unique_code', storage_id)
        found = storages.filter(storages.data, filter_)
        if not found:
            raise operation_exception("Storage not found")
        old_storage = found[0]
        old_storage.name = updated_storage.name
        old_storage.address = updated_storage.address
        self.__repo.save()

    def delete_storage(self, storage_id: str):
        validator.validate(storage_id, str)
        storages = prototype(self.__repo.data[reposity_manager.storage_key()])
        filter_ = filter_dto.create_equals_filter('unique_code', storage_id)
        found = storages.filter(storages.data, filter_)
        if not found:
            raise operation_exception("Storage not found")
        storage = found[0]
        observe_service.create_event(event_type.delete_storage(), {'storage': storage})
        self.__repo.data[reposity_manager.storage_key()].remove(storage)
        self.__repo.save()

    def get_storage(self, storage_id: str) -> storage_model:
        validator.validate(storage_id, str)
        storages = prototype(self.__repo.data[reposity_manager.storage_key()])
        filter_ = filter_dto.create_equals_filter('unique_code', storage_id)
        found = storages.filter(storages.data, filter_)
        if not found:
            return None
        return found[0]

    def create_group_from_dto(self, data: dict):
        dto = category_dto().create(data)
        cache = self.__get_cache()
        group = group_model.from_dto(dto, cache)
        if dto.id.strip() == "":
            pass
        return group

    def create_range_from_dto(self, data: dict):
        dto = range_dto().create(data)
        cache = self.__get_cache()
        range_ = range_model.from_dto(dto, cache)
        if dto.id.strip() == "":
            pass
        return range_

    def create_nomenclature_from_dto(self, data: dict):
        dto = nomenclature_dto().create(data)
        cache = self.__get_cache()
        nom = nomenclature_model.from_dto(dto, cache)
        if dto.id.strip() == "":
            pass
        return nom

    def create_storage_from_dto(self, data: dict):
        dto = storage_dto().create(data)
        cache = self.__get_cache()
        storage = storage_model.from_dto(dto, cache)
        if dto.id.strip() == "":
            pass
        return storage