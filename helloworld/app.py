from chalice import Chalice, Response
from chalice import BadRequestError
from chalice import NotFoundError
from urllib.parse import urlparse, parse_qs

app = Chalice(app_name='helloworld')
app.debug = True


@app.route('/')
def index():
    return {'hello': 'world'}


@app.route('/hello/{name}')
def index(name):
    return {'hello': name}


CITIES_TO_STATE = {
    'seattle': 'WA',
    'portland': 'OR',
}


@app.route('/cities/{city}')
def state_of_city(city: str) -> dict:
    try:
        return {'state': CITIES_TO_STATE[city]}
    except KeyError:
        raise BadRequestError("Unknown city '%s', valid choices are: %s" % (
            city, ', '.join(CITIES_TO_STATE.keys())))


@app.route('/resource/{value}', methods=['PUT'])
def put_test(value):
    return {"value": value}


@app.route('/myview', methods=['POST', 'PUT'])
def myview():
    pass


@app.route('/myview2', methods=['POST'])
def myview_post():
    pass


@app.route('/myview2', methods=['PUT'])
def myview_put():
    pass


OBJECTS = {}


@app.route('/objects/{key}', methods=['GET', 'PUT'])
def myobject(key):
    if app.current_request.method == 'PUT':
        OBJECTS[key] = app.current_request.json_body
        return Response(body={"success": True}, status_code=201)
    elif app.current_request.method == 'GET':
        try:
            return OBJECTS[key]
        except KeyError:
            raise NotFoundError(key)


@app.route('/introspect')
def introspect():
    return app.current_request.to_dict()


@app.route('/', methods=['POST'], content_types=['application/x-www-form-urlencoded'])
def index():
    parsed = parse_qs(app.current_request.raw_body.decode())
    return {'raw_body_decoded': parsed}

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
