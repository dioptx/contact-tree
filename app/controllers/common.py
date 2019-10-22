import json
import flask
def json_content_type():
    return {'Content-Type':'application/json'}

def ok(x = {}):
    return json.dumps(x), 200, json_content_type()

def error(x = ''):
    return json.dumps({'error': x}), 400, json_content_type()

def not_found():
    return '', 404


def req_to_json(req):
    if req == '':
        return error('No json data sent.')

    try:
        json_req = json.loads(req)
    except json.decoder.JSONDecodeError as er:
        return error("Could not decode JSON. "
                     "Error: " + str(er))
    return json_req


