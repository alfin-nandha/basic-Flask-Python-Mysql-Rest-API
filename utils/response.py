from flask import jsonify

def success_operation():
    return jsonify({
        'message':'success',
        'code': 200
        }), 200

def success_create():
    return jsonify({
        'message':'insert success',
        'code': 201
        }), 201

def success_update():
    return jsonify({
        'message':'update success',
        'code': 203
        }), 203

def email_already_exist():
    return jsonify({
        'message':'email already registered',
        'code': 403
        }), 403

def internal_service_error():
    return jsonify({
        'message': 'something went wrong',
        'code': 500
        }), 500

def success_get_data(data):
    return jsonify({
        'message':'success',
        'data': data,
        'code': 200
    }), 200

def fail_data_not_found():
    return jsonify({
        'message':'data not found',
        'code': 404
        }), 200