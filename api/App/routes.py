from api.App.PythonRevolution import Revolution_main as RevoMain
from api.App.models import Counter
from api.App import db
from api.AbilityBook import AbilityBook
from flask import url_for, render_template, request, Blueprint, redirect, send_from_directory
from flask import make_response, jsonify, send_file
from flask_cors import CORS
import os
import time
import pprint


api = Blueprint('api', __name__)
CORS(api, resources={r"/api/*": {"origins": "*"}}, support_credentials=True)


@api.route('/itemIDs', methods=['GET'])
def itemIDs():
    path = "itemIDs.json"
    return send_file(path, as_attachment=True, cache_timeout=0)


@api.route('/return_counter', methods=['GET'])
def return_counter():
    N = Counter.query.filter_by(name="RevolutionCounter").first()
    result = {'counter': N.count}
    res = make_response(jsonify(result), 200)

    res.headers.add("Access-Control-Allow-Origin", "*")
    return res


@api.route('/downloadJSON', methods=['GET'])
def downloadJSON():
    path = "itemIDs.json"
    return send_from_directory('./', path, as_attachment=True)


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
                user_input[key] = 0

    start_loop = time.time()

    CalcResults, warning, error_message = RevoMain.fight_dummy(user_input, AbilityBook)

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