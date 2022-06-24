from api.App.PythonRevolution import Revolution_main as RevoMain
# from api.App.PythonRotation import Rotation_main as RotMain
from api.App.models import Counter
from api.App import db
from ..GenerateObjects import Objects, NameList
# from api.App.PythonRevolution.Objects.GenerateObjects import Objects
from flask import url_for, request, Blueprint, send_from_directory
from flask import make_response, jsonify, send_file
from flask_cors import CORS
import os
import time

api = Blueprint('api', __name__)
CORS(api, resources={r"/api/*": {"origins": "*"}}, support_credentials=True)


@api.route('/itemIDs', methods=['GET'])
def itemIDs():
    path = "itemIDs.json"
    return send_file(path, as_attachment=True, cache_timeout=0)


@api.route('/return_counter', methods=['GET'])
def return_counter():
    N = Counter.query.filter_by(name="RevolutionCounter").first()
    result = {
        'counter': N.count,
        'nameList': NameList
    }
    res = make_response(jsonify(result), 200)

    res.headers.add("Access-Control-Allow-Origin", "*")
    return res


@api.route('/downloadJSON', methods=['GET'])
def downloadJSON():
    path = "itemIDs.json"
    return send_from_directory('./', path, as_attachment=True)


# @api.route("/save", methods=['POST'])
# def save():
#     userData = request.get_json()
#
#     print(userData['list']['title'])
#
#     foundList = List.query.filter_by(title=userData['list']['title']).first()
#
#     if foundList is None:
#         results = {
#             'error': True,
#             'error_message': f'List with title "{userData["list"]["title"]}" does not exist'
#         }
#
#         res = make_response(jsonify(results), 200)
#
#         return res
#
#     foundList.json = userData['list']
#     db.session.commit()
#
#     results = {
#         'status': 'success'
#     }
#
#     res = make_response(jsonify(results), 200)
#
#     return res
#
#
# @api.route("/get", methods=['POST'])
# def get():
#     userData = request.get_json()
#
#     foundList = List.query.filter_by(title=userData['title']).first()
#
#     if foundList is None:
#         results = {
#             'error': True,
#             'error_message': f'List with title "{userData["title"]}" does not exist'
#         }
#
#         res = make_response(jsonify(results), 200)
#
#         return res
#
#     results = {
#         'list': foundList.json
#     }
#
#     res = make_response(jsonify(results), 200)
#
#     return res
#
#
# @api.route("/create", methods=['POST'])
# def create():
#     userData = request.get_json()
#     print('hi', userData['title'])
#     foundList = List.query.filter_by(title=userData['title']).first()
#
#     if foundList is not None:
#         results = {
#             'error': True,
#             'error_message': 'Duplicate title'
#         }
#
#         res = make_response(jsonify(results), 200)
#
#         return res
#     print('hi', userData['title'])
#     N = Counter.query.filter_by(name="ListCounter").first()
#     N.count = N.count + 1
#
#     # # List.__table__.drop()
#     # # List.__table__.create(db.session.bind)
#
#     listStart = {
#         'title': userData['title'],
#         'id': N.count,
#         'counter': 0,
#         'categories': []
#     }
#
#     newList = List(id=N.count, title=userData['title'], json=listStart)
#     db.session.add(newList)
#
#     db.session.commit()
#
#     results = {
#         'list': listStart
#     }
#
#     res = make_response(jsonify(results), 200)
#
#     return res


@api.route("/calc", methods=['POST'])
def calc():
    user_input = request.get_json()

    user_rot = []

    # For each ability the user put on the bar
    for ability in user_input['Abilities']:
        # Replace underscore with whitespace to be compatible with rest of script
        user_rot.append(ability.replace('_', ' '))

    # Replace the rotation with newly formatted rotation
    user_input['Abilities'] = user_rot

    # For every input check if string is float and convert
    for key, value in user_input.items():
        isFloat = True

        if key != 'Abilities':  # Don't check ability entry since its an array
            try:
                float(value)
            except ValueError:
                isFloat = False

            if isFloat:
                user_input[key] = float(user_input[key])
            elif user_input[key] == "":
                if key == 'Adrenaline':
                    user_input[key] = -1
                else:
                    user_input[key] = 0

    warning = ''
    error_message = None
    CalcResults = {}

    start_loop = time.time()

    try:
        CalcResults = RevoMain.fight_dummy(user_input, Objects)
    except Exception as e:
        error_message = 'Error: ' + str(e)

    end_loop = time.time()

    N = Counter.query.filter_by(name="RevolutionCounter").first()

    if error_message is not None:
        error = True
    else:
        error = False

        N.count = N.count + 1
        db.session.commit()

    CalcResults.update({'ExecutionTime': round(end_loop - start_loop, 5),
                        'warning': warning,
                        'error': error,
                        'error_message': error_message,
                        'counter': N.count})

    res = make_response(jsonify(CalcResults), 200)

    return res


# @api.route("/calcRot", methods=['POST'])
# def calcRot():
#     user_input = request.get_json()
#
#     user_rot = []
#
#     # For each ability the user put on the bar
#     for i, ability in enumerate(user_input['Abilities']):
#         # Replace underscore with whitespace to be compatible with rest of script
#         if user_input['Abilities'][i] is not None:
#             ability['Name'] = ability['Name'].replace('_', ' ')
#
#             # For every option check if string is float and convert
#             for key, value in ability.items():
#                 isFloat = True
#
#                 try:
#                     float(value)
#                 except ValueError:
#                     isFloat = False
#
#                 if isFloat:
#                     ability[key] = float(ability[key])
#                 elif ability[key] in {"", "null"}:
#                     ability[key] = 0
#
#             user_rot.append(ability)
#
#     user_input['Abilities'] = user_rot
#
#     # For every input check if string is float and convert
#     for key, value in user_input.items():
#         isFloat = True
#
#         if key != 'Abilities':  # Don't check ability entry since its an array
#             try:
#                 float(value)
#             except ValueError:
#                 isFloat = False
#
#             if isFloat:
#                 user_input[key] = float(user_input[key])
#             elif user_input[key] == "":
#                 user_input[key] = 0
#
#     start_loop = time.time()
#
#     warning = ''
#     error_message = ''
#     CalcResults = {}
#
#     # try:
#     CalcResults, warning, error_message = RotMain.fight_dummy(user_input, RotationAbilityBook)
#     # except Exception as e:
#     #     error_message = 'Error: ' + str(e)
#
#     end_loop = time.time()
#
#     N = Counter.query.filter_by(name="RevolutionCounter").first()
#
#     if error_message is not None:
#         error = True
#     else:
#         error = False
#
#         N.count = N.count + 1
#         db.session.commit()
#
#     CalcResults.update({'ExecutionTime': round(end_loop - start_loop, 5),
#                         'warning': warning,
#                         'error': error,
#                         'error_message': error_message,
#                         'counter': N.count})
#
#     res = make_response(jsonify(CalcResults), 200)
#
#     return res


@api.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(api.root_path, endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)