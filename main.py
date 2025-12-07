import connexion
from flask import request, jsonify
from Src.Logics.reference_service import reference_service
from Src.Logics.convert_factory import convert_factory
from Src.Core.validator import operation_exception
from Src.Logics.reference_observer_service import reference_observer_service
from Src.Logics.settings_observer_service import settings_observer_service
from Src.start_manager import start_manager
from Src.Core.observe_service import observe_service
from Src.Core.event_type import event_type
from Src.Core.log_level import log_level
from Src.Logics.log_observer import log_observer

app = connexion.FlaskApp(__name__)

"""
Проверить доступность REST API
"""
@app.route("/api/accessibility", methods=['GET'])
def formats():
    observe_service.create_event(event_type.log_info(), {
        'level': log_level.INFO, 'message': 'Web call: accessibility', 'context': {'method': 'GET', 'path': '/api/accessibility'}
    })
    return "SUCCESS"

@app.route("/api/group/<group_id>", methods=['GET'])
def get_group(group_id):
    observe_service.create_event(event_type.log_debug(), {
        'level': log_level.DEBUG, 'message': 'Web call: get_group', 'context': {'method': 'GET', 'path': f'/api/group/{group_id}'}
    })
    service = reference_service()
    group = service.get_group(group_id)
    if group is None:
        observe_service.create_event(event_type.log_info(), {
            'level': log_level.INFO, 'message': 'Group not found', 'context': {'group_id': group_id}
        })
        return "Not found", 404
    factory = convert_factory()
    observe_service.create_event(event_type.log_info(), {
        'level': log_level.INFO, 'message': 'Group retrieved', 'context': {'group_id': group_id}
    })
    return jsonify(factory.serialize(group.to_dto()))

@app.route("/api/group", methods=['PUT'])
def add_group():
    data = request.json
    observe_service.create_event(event_type.log_debug(), {
        'level': log_level.DEBUG, 'message': 'Web call: add_group', 'context': {'method': 'PUT', 'path': '/api/group'}
    })
    service = reference_service()
    try:
        group = service.create_group_from_dto(data)
        service.add_group(group)
        factory = convert_factory()
        observe_service.create_event(event_type.log_info(), {
            'level': log_level.INFO, 'message': 'Group added', 'context': {'id': group.unique_code, 'name': group.name}
        })
        return jsonify(factory.serialize(group.to_dto()))
    except operation_exception as e:
        observe_service.create_event(event_type.log_error(), {
            'level': log_level.ERROR, 'message': 'Group add failed', 'context': {'error': str(e)}
        })
        return str(e), 400

@app.route("/api/group/<group_id>", methods=['PATCH'])
def update_group(group_id):
    data = request.json
    observe_service.create_event(event_type.log_debug(), {
        'level': log_level.DEBUG, 'message': 'Web call: update_group', 'context': {'method': 'PATCH', 'path': f'/api/group/{group_id}'}
    })
    service = reference_service()
    try:
        updated_group = service.create_group_from_dto(data)
        service.update_group(group_id, updated_group)
        observe_service.create_event(event_type.log_info(), {
            'level': log_level.INFO, 'message': 'Group updated', 'context': {'group_id': group_id}
        })
        return "Updated"
    except operation_exception as e:
        observe_service.create_event(event_type.log_error(), {
            'level': log_level.ERROR, 'message': 'Group update failed', 'context': {'group_id': group_id, 'error': str(e)}
        })
        return str(e), 400

@app.route("/api/group/<group_id>", methods=['DELETE'])
def delete_group(group_id):
    observe_service.create_event(event_type.log_debug(), {
        'level': log_level.DEBUG, 'message': 'Web call: delete_group', 'context': {'method': 'DELETE', 'path': f'/api/group/{group_id}'}
    })
    service = reference_service()
    try:
        service.delete_group(group_id)
        observe_service.create_event(event_type.log_info(), {
            'level': log_level.INFO, 'message': 'Group deleted', 'context': {'group_id': group_id}
        })
        return "Deleted"
    except operation_exception as e:
        observe_service.create_event(event_type.log_error(), {
            'level': log_level.ERROR, 'message': 'Group delete failed', 'context': {'group_id': group_id, 'error': str(e)}
        })
        return str(e), 400

@app.route("/api/range/<range_id>", methods=['GET'])
def get_range(range_id):
    observe_service.create_event(event_type.log_debug(), {
        'level': log_level.DEBUG, 'message': 'Web call: get_range', 'context': {'method': 'GET', 'path': f'/api/range/{range_id}'}
    })
    service = reference_service()
    range_ = service.get_range(range_id)
    if range_ is None:
        observe_service.create_event(event_type.log_info(), {
            'level': log_level.INFO, 'message': 'Range not found', 'context': {'range_id': range_id}
        })
        return "Not found", 404
    factory = convert_factory()
    observe_service.create_event(event_type.log_info(), {
        'level': log_level.INFO, 'message': 'Range retrieved', 'context': {'range_id': range_id}
    })
    return jsonify(factory.serialize(range_.to_dto()))

@app.route("/api/range", methods=['PUT'])
def add_range():
    data = request.json
    observe_service.create_event(event_type.log_debug(), {
        'level': log_level.DEBUG, 'message': 'Web call: add_range', 'context': {'method': 'PUT', 'path': '/api/range'}
    })
    service = reference_service()
    try:
        range_ = service.create_range_from_dto(data)
        service.add_range(range_)
        factory = convert_factory()
        observe_service.create_event(event_type.log_info(), {
            'level': log_level.INFO, 'message': 'Range added', 'context': {'id': range_.unique_code, 'name': range_.name}
        })
        return jsonify(factory.serialize(range_.to_dto()))
    except operation_exception as e:
        observe_service.create_event(event_type.log_error(), {
            'level': log_level.ERROR, 'message': 'Range add failed', 'context': {'error': str(e)}
        })
        return str(e), 400

@app.route("/api/range/<range_id>", methods=['PATCH'])
def update_range(range_id):
    data = request.json
    observe_service.create_event(event_type.log_debug(), {
        'level': log_level.DEBUG, 'message': 'Web call: update_range', 'context': {'method': 'PATCH', 'path': f'/api/range/{range_id}'}
    })
    service = reference_service()
    try:
        updated_range = service.create_range_from_dto(data)
        service.update_range(range_id, updated_range)
        observe_service.create_event(event_type.log_info(), {
            'level': log_level.INFO, 'message': 'Range updated', 'context': {'range_id': range_id}
        })
        return "Updated"
    except operation_exception as e:
        observe_service.create_event(event_type.log_error(), {
            'level': log_level.ERROR, 'message': 'Range update failed', 'context': {'range_id': range_id, 'error': str(e)}
        })
        return str(e), 400

@app.route("/api/range/<range_id>", methods=['DELETE'])
def delete_range(range_id):
    observe_service.create_event(event_type.log_debug(), {
        'level': log_level.DEBUG, 'message': 'Web call: delete_range', 'context': {'method': 'DELETE', 'path': f'/api/range/{range_id}'}
    })
    service = reference_service()
    try:
        service.delete_range(range_id)
        observe_service.create_event(event_type.log_info(), {
            'level': log_level.INFO, 'message': 'Range deleted', 'context': {'range_id': range_id}
        })
        return "Deleted"
    except operation_exception as e:
        observe_service.create_event(event_type.log_error(), {
            'level': log_level.ERROR, 'message': 'Range delete failed', 'context': {'range_id': range_id, 'error': str(e)}
        })
        return str(e), 400

@app.route("/api/nomenclature/<nom_id>", methods=['GET'])
def get_nomenclature(nom_id):
    observe_service.create_event(event_type.log_debug(), {
        'level': log_level.DEBUG, 'message': 'Web call: get_nomenclature', 'context': {'method': 'GET', 'path': f'/api/nomenclature/{nom_id}'}
    })
    service = reference_service()
    nom = service.get_nomenclature(nom_id)
    if nom is None:
        observe_service.create_event(event_type.log_info(), {
            'level': log_level.INFO, 'message': 'Nomenclature not found', 'context': {'nom_id': nom_id}
        })
        return "Not found", 404
    factory = convert_factory()
    observe_service.create_event(event_type.log_info(), {
        'level': log_level.INFO, 'message': 'Nomenclature retrieved', 'context': {'nom_id': nom_id}
    })
    return jsonify(factory.serialize(nom.to_dto()))

@app.route("/api/nomenclature", methods=['PUT'])
def add_nomenclature():
    data = request.json
    observe_service.create_event(event_type.log_debug(), {
        'level': log_level.DEBUG, 'message': 'Web call: add_nomenclature', 'context': {'method': 'PUT', 'path': '/api/nomenclature'}
    })
    service = reference_service()
    try:
        nom = service.create_nomenclature_from_dto(data)
        service.add_nomenclature(nom)
        factory = convert_factory()
        observe_service.create_event(event_type.log_info(), {
            'level': log_level.INFO, 'message': 'Nomenclature added', 'context': {'id': nom.unique_code, 'name': nom.name}
        })
        return jsonify(factory.serialize(nom.to_dto()))
    except operation_exception as e:
        observe_service.create_event(event_type.log_error(), {
            'level': log_level.ERROR, 'message': 'Nomenclature add failed', 'context': {'error': str(e)}
        })
        return str(e), 400

@app.route("/api/nomenclature/<nom_id>", methods=['PATCH'])
def update_nomenclature(nom_id):
    data = request.json
    observe_service.create_event(event_type.log_debug(), {
        'level': log_level.DEBUG, 'message': 'Web call: update_nomenclature', 'context': {'method': 'PATCH', 'path': f'/api/nomenclature/{nom_id}'}
    })
    service = reference_service()
    try:
        updated_nom = service.create_nomenclature_from_dto(data)
        service.update_nomenclature(nom_id, updated_nom)
        observe_service.create_event(event_type.log_info(), {
            'level': log_level.INFO, 'message': 'Nomenclature updated', 'context': {'nom_id': nom_id}
        })
        return "Updated"
    except operation_exception as e:
        observe_service.create_event(event_type.log_error(), {
            'level': log_level.ERROR, 'message': 'Nomenclature update failed', 'context': {'nom_id': nom_id, 'error': str(e)}
        })
        return str(e), 400

@app.route("/api/nomenclature/<nom_id>", methods=['DELETE'])
def delete_nomenclature(nom_id):
    observe_service.create_event(event_type.log_debug(), {
        'level': log_level.DEBUG, 'message': 'Web call: delete_nomenclature', 'context': {'method': 'DELETE', 'path': f'/api/nomenclature/{nom_id}'}
    })
    service = reference_service()
    try:
        service.delete_nomenclature(nom_id)
        observe_service.create_event(event_type.log_info(), {
            'level': log_level.INFO, 'message': 'Nomenclature deleted', 'context': {'nom_id': nom_id}
        })
        return "Deleted"
    except operation_exception as e:
        observe_service.create_event(event_type.log_error(), {
            'level': log_level.ERROR, 'message': 'Nomenclature delete failed', 'context': {'nom_id': nom_id, 'error': str(e)}
        })
        return str(e), 400

@app.route("/api/storage/<storage_id>", methods=['GET'])
def get_storage(storage_id):
    observe_service.create_event(event_type.log_debug(), {
        'level': log_level.DEBUG, 'message': 'Web call: get_storage', 'context': {'method': 'GET', 'path': f'/api/storage/{storage_id}'}
    })
    service = reference_service()
    storage = service.get_storage(storage_id)
    if storage is None:
        observe_service.create_event(event_type.log_info(), {
            'level': log_level.INFO, 'message': 'Storage not found', 'context': {'storage_id': storage_id}
        })
        return "Not found", 404
    factory = convert_factory()
    observe_service.create_event(event_type.log_info(), {
        'level': log_level.INFO, 'message': 'Storage retrieved', 'context': {'storage_id': storage_id}
    })
    return jsonify(factory.serialize(storage.to_dto()))

@app.route("/api/storage", methods=['PUT'])
def add_storage():
    data = request.json
    observe_service.create_event(event_type.log_debug(), {
        'level': log_level.DEBUG, 'message': 'Web call: add_storage', 'context': {'method': 'PUT', 'path': '/api/storage'}
    })
    service = reference_service()
    try:
        storage = service.create_storage_from_dto(data)
        service.add_storage(storage)
        factory = convert_factory()
        observe_service.create_event(event_type.log_info(), {
            'level': log_level.INFO, 'message': 'Storage added', 'context': {'id': storage.unique_code, 'name': storage.name}
        })
        return jsonify(factory.serialize(storage.to_dto()))
    except operation_exception as e:
        observe_service.create_event(event_type.log_error(), {
            'level': log_level.ERROR, 'message': 'Storage add failed', 'context': {'error': str(e)}
        })
        return str(e), 400

@app.route("/api/storage/<storage_id>", methods=['PATCH'])
def update_storage(storage_id):
    data = request.json
    observe_service.create_event(event_type.log_debug(), {
        'level': log_level.DEBUG, 'message': 'Web call: update_storage', 'context': {'method': 'PATCH', 'path': f'/api/storage/{storage_id}'}
    })
    service = reference_service()
    try:
        updated_storage = service.create_storage_from_dto(data)
        service.update_storage(storage_id, updated_storage)
        observe_service.create_event(event_type.log_info(), {
            'level': log_level.INFO, 'message': 'Storage updated', 'context': {'storage_id': storage_id}
        })
        return "Updated"
    except operation_exception as e:
        observe_service.create_event(event_type.log_error(), {
            'level': log_level.ERROR, 'message': 'Storage update failed', 'context': {'storage_id': storage_id, 'error': str(e)}
        })
        return str(e), 400

@app.route("/api/storage/<storage_id>", methods=['DELETE'])
def delete_storage(storage_id):
    observe_service.create_event(event_type.log_debug(), {
        'level': log_level.DEBUG, 'message': 'Web call: delete_storage', 'context': {'method': 'DELETE', 'path': f'/api/storage/{storage_id}'}
    })
    service = reference_service()
    try:
        service.delete_storage(storage_id)
        observe_service.create_event(event_type.log_info(), {
            'level': log_level.INFO, 'message': 'Storage deleted', 'context': {'storage_id': storage_id}
        })
        return "Deleted"
    except operation_exception as e:
        observe_service.create_event(event_type.log_error(), {
            'level': log_level.ERROR, 'message': 'Storage delete failed', 'context': {'storage_id': storage_id, 'error': str(e)}
        })
        return str(e), 400

if __name__ == '__main__':
    reference_observer_service()
    settings_observer_service()
    logger = log_observer("settings.json")
    observe_service.add(logger)
    start_manager().start()
    app.run(host="0.0.0.0", port = 8080)
