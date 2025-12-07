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
from Src.Core.log_level import log_level

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
        observe_service.create_event(event_type.log_debug(), {
            'level': log_level.DEBUG, 'message': 'add_group called', 'context': {'group_name': getattr(group, 'name', '')}
        })
        validator.validate(group, group_model)
        self.__repo.data[reposity_manager.group_key()].append(group)
        self.__repo.save()
        observe_service.create_event(event_type.log_info(), {
            'level': log_level.INFO, 'message': 'Group added', 'context': {'id': group.unique_code, 'name': group.name}
        })

    def update_group(self, group_id: str, updated_group: group_model):
        observe_service.create_event(event_type.log_debug(), {
            'level': log_level.DEBUG, 'message': 'update_group called', 'context': {'group_id': group_id}
        })
        validator.validate(group_id, str)
        validator.validate(updated_group, group_model)
        groups = prototype(self.__repo.data[reposity_manager.group_key()])
        filter_ = filter_dto.create_equals_filter('unique_code', group_id)
        found = groups.filter(groups.data, filter_)
        if not found:
            observe_service.create_event(event_type.log_error(), {
                'level': log_level.ERROR, 'message': 'Group not found', 'context': {'group_id': group_id}
            })
            raise operation_exception("Group not found")
        old_group = found[0]
        old_group.name = updated_group.name
        self.__repo.save()
        observe_service.create_event(event_type.log_info(), {
            'level': log_level.INFO, 'message': 'Group updated', 'context': {'group_id': group_id, 'new_name': updated_group.name}
        })

    def delete_group(self, group_id: str):
        observe_service.create_event(event_type.log_debug(), {
            'level': log_level.DEBUG, 'message': 'delete_group called', 'context': {'group_id': group_id}
        })
        validator.validate(group_id, str)
        groups = prototype(self.__repo.data[reposity_manager.group_key()])
        filter_ = filter_dto.create_equals_filter('unique_code', group_id)
        found = groups.filter(groups.data, filter_)
        if not found:
            observe_service.create_event(event_type.log_error(), {
                'level': log_level.ERROR, 'message': 'Group not found', 'context': {'group_id': group_id}
            })
            raise operation_exception("Group not found")
        group = found[0]
        observe_service.create_event(event_type.delete_group(), {'group': group})
        self.__repo.data[reposity_manager.group_key()].remove(group)
        self.__repo.save()
        observe_service.create_event(event_type.log_info(), {
            'level': log_level.INFO, 'message': 'Group deleted', 'context': {'group_id': group_id}
        })

    def get_group(self, group_id: str) -> group_model:
        observe_service.create_event(event_type.log_debug(), {
            'level': log_level.DEBUG, 'message': 'get_group called', 'context': {'group_id': group_id}
        })
        validator.validate(group_id, str)
        groups = prototype(self.__repo.data[reposity_manager.group_key()])
        filter_ = filter_dto.create_equals_filter('unique_code', group_id)
        found = groups.filter(groups.data, filter_)
        if not found:
            observe_service.create_event(event_type.log_info(), {
                'level': log_level.INFO, 'message': 'Group not found result', 'context': {'group_id': group_id}
            })
            return None
        observe_service.create_event(event_type.log_info(), {
            'level': log_level.INFO, 'message': 'Group retrieved', 'context': {'group_id': group_id}
        })
        return found[0]

    def add_range(self, range_: range_model):
        observe_service.create_event(event_type.log_debug(), {
            'level': log_level.DEBUG, 'message': 'add_range called', 'context': {'name': getattr(range_, 'name', '')}
        })
        validator.validate(range_, range_model)
        self.__repo.data[reposity_manager.range_key()].append(range_)
        self.__repo.save()
        observe_service.create_event(event_type.log_info(), {
            'level': log_level.INFO, 'message': 'Range added', 'context': {'id': range_.unique_code, 'name': range_.name}
        })

    def update_range(self, range_id: str, updated_range: range_model):
        observe_service.create_event(event_type.log_debug(), {
            'level': log_level.DEBUG, 'message': 'update_range called', 'context': {'range_id': range_id}
        })
        validator.validate(range_id, str)
        validator.validate(updated_range, range_model)
        ranges = prototype(self.__repo.data[reposity_manager.range_key()])
        filter_ = filter_dto.create_equals_filter('unique_code', range_id)
        found = ranges.filter(ranges.data, filter_)
        if not found:
            observe_service.create_event(event_type.log_error(), {
                'level': log_level.ERROR, 'message': 'Range not found', 'context': {'range_id': range_id}
            })
            raise operation_exception("Range not found")
        old_range = found[0]
        old_range.name = updated_range.name
        old_range.value = updated_range.value
        old_range.base = updated_range.base
        self.__repo.save()
        observe_service.create_event(event_type.log_info(), {
            'level': log_level.INFO, 'message': 'Range updated',
            'context': {'range_id': range_id, 'new_name': updated_range.name, 'new_value': updated_range.value}
        })

    def delete_range(self, range_id: str):
        observe_service.create_event(event_type.log_debug(), {
            'level': log_level.DEBUG, 'message': 'delete_range called', 'context': {'range_id': range_id}
        })
        validator.validate(range_id, str)
        ranges = prototype(self.__repo.data[reposity_manager.range_key()])
        filter_ = filter_dto.create_equals_filter('unique_code', range_id)
        found = ranges.filter(ranges.data, filter_)
        if not found:
            observe_service.create_event(event_type.log_error(), {
                'level': log_level.ERROR, 'message': 'Range not found', 'context': {'range_id': range_id}
            })
            raise operation_exception("Range not found")
        range_ = found[0]
        observe_service.create_event(event_type.delete_range(), {'range': range_})
        self.__repo.data[reposity_manager.range_key()].remove(range_)
        self.__repo.save()
        observe_service.create_event(event_type.log_info(), {
            'level': log_level.INFO, 'message': 'Range deleted', 'context': {'range_id': range_id}
        })

    def get_range(self, range_id: str) -> range_model:
        observe_service.create_event(event_type.log_debug(), {
            'level': log_level.DEBUG, 'message': 'get_range called', 'context': {'range_id': range_id}
        })
        validator.validate(range_id, str)
        ranges = prototype(self.__repo.data[reposity_manager.range_key()])
        filter_ = filter_dto.create_equals_filter('unique_code', range_id)
        found = ranges.filter(ranges.data, filter_)
        if not found:
            observe_service.create_event(event_type.log_info(), {
                'level': log_level.INFO, 'message': 'Range not found result', 'context': {'range_id': range_id}
            })
            return None
        observe_service.create_event(event_type.log_info(), {
            'level': log_level.INFO, 'message': 'Range retrieved', 'context': {'range_id': range_id}
        })
        return found[0]

    def add_nomenclature(self, nom: nomenclature_model):
        observe_service.create_event(event_type.log_debug(), {
            'level': log_level.DEBUG, 'message': 'add_nomenclature called', 'context': {'name': getattr(nom, 'name', '')}
        })
        validator.validate(nom, nomenclature_model)
        self.__repo.data[reposity_manager.nomenclature_key()].append(nom)
        self.__repo.save()
        observe_service.create_event(event_type.log_info(), {
            'level': log_level.INFO, 'message': 'Nomenclature added', 'context': {'id': nom.unique_code, 'name': nom.name}
        })

    def update_nomenclature(self, nom_id: str, updated_nom: nomenclature_model):
        observe_service.create_event(event_type.log_debug(), {
            'level': log_level.DEBUG, 'message': 'update_nomenclature called', 'context': {'nom_id': nom_id}
        })
        validator.validate(nom_id, str)
        validator.validate(updated_nom, nomenclature_model)
        noms = prototype(self.__repo.data[reposity_manager.nomenclature_key()])
        filter_ = filter_dto.create_equals_filter('unique_code', nom_id)
        found = noms.filter(noms.data, filter_)
        if not found:
            observe_service.create_event(event_type.log_error(), {
                'level': log_level.ERROR, 'message': 'Nomenclature not found', 'context': {'nom_id': nom_id}
            })
            raise operation_exception("Nomenclature not found")
        old_nom = found[0]
        old_nom.name = updated_nom.name
        old_nom.group = updated_nom.group
        old_nom.range = updated_nom.range
        self.__repo.save()
        observe_service.create_event(event_type.log_info(), {
            'level': log_level.INFO, 'message': 'Nomenclature updated',
            'context': {'nom_id': nom_id, 'new_name': updated_nom.name}
        })

    def delete_nomenclature(self, nom_id: str):
        observe_service.create_event(event_type.log_debug(), {
            'level': log_level.DEBUG, 'message': 'delete_nomenclature called', 'context': {'nom_id': nom_id}
        })
        validator.validate(nom_id, str)
        noms = prototype(self.__repo.data[reposity_manager.nomenclature_key()])
        filter_ = filter_dto.create_equals_filter('unique_code', nom_id)
        found = noms.filter(noms.data, filter_)
        if not found:
            observe_service.create_event(event_type.log_error(), {
                'level': log_level.ERROR, 'message': 'Nomenclature not found', 'context': {'nom_id': nom_id}
            })
            raise operation_exception("Nomenclature not found")
        nom = found[0]
        observe_service.create_event(event_type.delete_nomenclature(), {'nomenclature': nom})
        self.__repo.data[reposity_manager.nomenclature_key()].remove(nom)
        self.__repo.save()
        observe_service.create_event(event_type.log_info(), {
            'level': log_level.INFO, 'message': 'Nomenclature deleted', 'context': {'nom_id': nom_id}
        })

    def get_nomenclature(self, nom_id: str) -> nomenclature_model:
        observe_service.create_event(event_type.log_debug(), {
            'level': log_level.DEBUG, 'message': 'get_nomenclature called', 'context': {'nom_id': nom_id}
        })
        validator.validate(nom_id, str)
        noms = prototype(self.__repo.data[reposity_manager.nomenclature_key()])
        filter_ = filter_dto.create_equals_filter('unique_code', nom_id)
        found = noms.filter(noms.data, filter_)
        if not found:
            observe_service.create_event(event_type.log_info(), {
                'level': log_level.INFO, 'message': 'Nomenclature not found result', 'context': {'nom_id': nom_id}
            })
            return None
        observe_service.create_event(event_type.log_info(), {
            'level': log_level.INFO, 'message': 'Nomenclature retrieved', 'context': {'nom_id': nom_id}
        })
        return found[0]

    def add_storage(self, storage: storage_model):
        observe_service.create_event(event_type.log_debug(), {
            'level': log_level.DEBUG, 'message': 'add_storage called', 'context': {'name': getattr(storage, 'name', '')}
        })
        validator.validate(storage, storage_model)
        self.__repo.data[reposity_manager.storage_key()].append(storage)
        self.__repo.save()
        observe_service.create_event(event_type.log_info(), {
            'level': log_level.INFO, 'message': 'Storage added', 'context': {'id': storage.unique_code, 'name': storage.name}
        })

    def update_storage(self, storage_id: str, updated_storage: storage_model):
        observe_service.create_event(event_type.log_debug(), {
            'level': log_level.DEBUG, 'message': 'update_storage called', 'context': {'storage_id': storage_id}
        })
        validator.validate(storage_id, str)
        validator.validate(updated_storage, storage_model)
        storages = prototype(self.__repo.data[reposity_manager.storage_key()])  
        filter_ = filter_dto.create_equals_filter('unique_code', storage_id)
        found = storages.filter(storages.data, filter_)
        if not found:
            observe_service.create_event(event_type.log_error(), {
                'level': log_level.ERROR, 'message': 'Storage not found', 'context': {'storage_id': storage_id}
            })
            raise operation_exception("Storage not found")
        old_storage = found[0]
        old_storage.name = updated_storage.name
        old_storage.address = updated_storage.address
        self.__repo.save()
        observe_service.create_event(event_type.log_info(), {
            'level': log_level.INFO, 'message': 'Storage updated',
            'context': {'storage_id': storage_id, 'new_name': updated_storage.name}
        })

    def delete_storage(self, storage_id: str):
        observe_service.create_event(event_type.log_debug(), {
            'level': log_level.DEBUG, 'message': 'delete_storage called', 'context': {'storage_id': storage_id}
        })
        validator.validate(storage_id, str)
        storages = prototype(self.__repo.data[reposity_manager.storage_key()])
        filter_ = filter_dto.create_equals_filter('unique_code', storage_id)
        found = storages.filter(storages.data, filter_)
        if not found:
            observe_service.create_event(event_type.log_error(), {
                'level': log_level.ERROR, 'message': 'Storage not found', 'context': {'storage_id': storage_id}
            })
            raise operation_exception("Storage not found")
        storage = found[0]
        observe_service.create_event(event_type.delete_storage(), {'storage': storage})
        self.__repo.data[reposity_manager.storage_key()].remove(storage)
        self.__repo.save()
        observe_service.create_event(event_type.log_info(), {
            'level': log_level.INFO, 'message': 'Storage deleted', 'context': {'storage_id': storage_id}
        })

    def get_storage(self, storage_id: str) -> storage_model:
        observe_service.create_event(event_type.log_debug(), {
            'level': log_level.DEBUG, 'message': 'get_storage called', 'context': {'storage_id': storage_id}
        })
        validator.validate(storage_id, str)
        storages = prototype(self.__repo.data[reposity_manager.storage_key()])
        filter_ = filter_dto.create_equals_filter('unique_code', storage_id)
        found = storages.filter(storages.data, filter_)
        if not found:
            observe_service.create_event(event_type.log_info(), {
                'level': log_level.INFO, 'message': 'Storage not found result', 'context': {'storage_id': storage_id}
            })
            return None
        observe_service.create_event(event_type.log_info(), {
            'level': log_level.INFO, 'message': 'Storage retrieved', 'context': {'storage_id': storage_id}
        })
        return found[0]

    def create_group_from_dto(self, data: dict):
        dto = category_dto().create(data)
        cache = self.__get_cache()
        group = group_model.from_dto(dto, cache)
        if dto.id.strip() == "":
            pass
        observe_service.create_event(event_type.log_debug(), {
            'level': log_level.DEBUG, 'message': 'Group created from DTO', 'context': {'id': dto.id, 'name': dto.name}
        })
        return group

    def create_range_from_dto(self, data: dict):
        dto = range_dto().create(data)
        cache = self.__get_cache()
        range_ = range_model.from_dto(dto, cache)
        if dto.id.strip() == "":
            pass
        observe_service.create_event(event_type.log_debug(), {
            'level': log_level.DEBUG, 'message': 'Range created from DTO', 'context': {'id': dto.id, 'name': dto.name}
        })
        return range_

    def create_nomenclature_from_dto(self, data: dict):
        dto = nomenclature_dto().create(data)
        cache = self.__get_cache()
        nom = nomenclature_model.from_dto(dto, cache)
        if dto.id.strip() == "":
            pass
        observe_service.create_event(event_type.log_debug(), {
            'level': log_level.DEBUG, 'message': 'Nomenclature created from DTO', 'context': {'id': dto.id, 'name': dto.name}
        })
        return nom

    def create_storage_from_dto(self, data: dict):
        dto = storage_dto().create(data)
        cache = self.__get_cache()
        storage = storage_model.from_dto(dto, cache)
        if dto.id.strip() == "":
            pass
        observe_service.create_event(event_type.log_debug(), {
            'level': log_level.DEBUG, 'message': 'Storage created from DTO', 'context': {'id': dto.id, 'name': dto.name}
        })
        return storage
