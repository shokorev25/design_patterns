import connexion
from flask import request, jsonify
from Src.Logics.reference_service import reference_service
from Src.Logics.convert_factory import convert_factory
from Src.Core.validator import operation_exception
from Src.Logics.reference_observer_service import reference_observer_service
from Src.Logics.settings_observer_service import settings_observer_service
from Src.start_manager import start_manager

app = connexion.FlaskApp(__name__)

"""
Проверить доступность REST API
"""
@app.route("/api/accessibility", methods=['GET'])
def formats():
    return "SUCCESS"

@app.route("/api/group/<group_id>", methods=['GET'])
def get_group(group_id):
    service = reference_service()
    group = service.get_group(group_id)
    if group is None:
        return "Not found", 404
    factory = convert_factory()
    return jsonify(factory.serialize(group.to_dto()))

@app.route("/api/group", methods=['PUT'])
def add_group():
    data = request.json
    service = reference_service()
    try:
        group = service.create_group_from_dto(data)
        service.add_group(group)
        factory = convert_factory()
        return jsonify(factory.serialize(group.to_dto()))
    except operation_exception as e:
        return str(e), 400

@app.route("/api/group/<group_id>", methods=['PATCH'])
def update_group(group_id):
    data = request.json
    service = reference_service()
    try:
        updated_group = service.create_group_from_dto(data)
        service.update_group(group_id, updated_group)
        return "Updated"
    except operation_exception as e:
        return str(e), 400

@app.route("/api/group/<group_id>", methods=['DELETE'])
def delete_group(group_id):
    service = reference_service()
    try:
        service.delete_group(group_id)
        return "Deleted"
    except operation_exception as e:
        return str(e), 400

@app.route("/api/range/<range_id>", methods=['GET'])
def get_range(range_id):
    service = reference_service()
    range_ = service.get_range(range_id)
    if range_ is None:
        return "Not found", 404
    factory = convert_factory()
    return jsonify(factory.serialize(range_.to_dto()))

@app.route("/api/range", methods=['PUT'])
def add_range():
    data = request.json
    service = reference_service()
    try:
        range_ = service.create_range_from_dto(data)
        service.add_range(range_)
        factory = convert_factory()
        return jsonify(factory.serialize(range_.to_dto()))
    except operation_exception as e:
        return str(e), 400

@app.route("/api/range/<range_id>", methods=['PATCH'])
def update_range(range_id):
    data = request.json
    service = reference_service()
    try:
        updated_range = service.create_range_from_dto(data)
        service.update_range(range_id, updated_range)
        return "Updated"
    except operation_exception as e:
        return str(e), 400

@app.route("/api/range/<range_id>", methods=['DELETE'])
def delete_range(range_id):
    service = reference_service()
    try:
        service.delete_range(range_id)
        return "Deleted"
    except operation_exception as e:
        return str(e), 400

@app.route("/api/nomenclature/<nom_id>", methods=['GET'])
def get_nomenclature(nom_id):
    service = reference_service()
    nom = service.get_nomenclature(nom_id)
    if nom is None:
        return "Not found", 404
    factory = convert_factory()
    return jsonify(factory.serialize(nom.to_dto()))

@app.route("/api/nomenclature", methods=['PUT'])
def add_nomenclature():
    data = request.json
    service = reference_service()
    try:
        nom = service.create_nomenclature_from_dto(data)
        service.add_nomenclature(nom)
        factory = convert_factory()
        return jsonify(factory.serialize(nom.to_dto()))
    except operation_exception as e:
        return str(e), 400

@app.route("/api/nomenclature/<nom_id>", methods=['PATCH'])
def update_nomenclature(nom_id):
    data = request.json
    service = reference_service()
    try:
        updated_nom = service.create_nomenclature_from_dto(data)
        service.update_nomenclature(nom_id, updated_nom)
        return "Updated"
    except operation_exception as e:
        return str(e), 400

@app.route("/api/nomenclature/<nom_id>", methods=['DELETE'])
def delete_nomenclature(nom_id):
    service = reference_service()
    try:
        service.delete_nomenclature(nom_id)
        return "Deleted"
    except operation_exception as e:
        return str(e), 400

@app.route("/api/storage/<storage_id>", methods=['GET'])
def get_storage(storage_id):
    service = reference_service()
    storage = service.get_storage(storage_id)
    if storage is None:
        return "Not found", 404
    factory = convert_factory()
    return jsonify(factory.serialize(storage.to_dto()))

@app.route("/api/storage", methods=['PUT'])
def add_storage():
    data = request.json
    service = reference_service()
    try:
        storage = service.create_storage_from_dto(data)
        service.add_storage(storage)
        factory = convert_factory()
        return jsonify(factory.serialize(storage.to_dto()))
    except operation_exception as e:
        return str(e), 400

@app.route("/api/storage/<storage_id>", methods=['PATCH'])
def update_storage(storage_id):
    data = request.json
    service = reference_service()
    try:
        updated_storage = service.create_storage_from_dto(data)
        service.update_storage(storage_id, updated_storage)
        return "Updated"
    except operation_exception as e:
        return str(e), 400

@app.route("/api/storage/<storage_id>", methods=['DELETE'])
def delete_storage(storage_id):
    service = reference_service()
    try:
        service.delete_storage(storage_id)
        return "Deleted"
    except operation_exception as e:
        return str(e), 400

if __name__ == '__main__':
    reference_observer_service()
    settings_observer_service()
    start_manager().start()
    app.run(host="0.0.0.0", port = 8080)
