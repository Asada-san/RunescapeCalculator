import flask
from flask import Flask, redirect, render_template, url_for, render_template, request
from flask import make_response, jsonify
import os
import json
import pprint
import Revolution_main as calcMain
import CombatChecks as CC
import AttackingPhase as Attack
import LoopObjects as CO
import AbilityObject
import pandas as pd
from AbilityBook import AbilityBook
import time

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/bar")
def bar():
    return render_template("bar.html")


@app.route("/home")
def ge():
    return render_template("index.html")


@app.route("/calc", methods=['POST'])
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

    start_loop = time.time()

    CalcResults, warning, error_message = calcMain.fight_dummy(user_input, AbilityBook)

    end_loop = time.time()

    if error_message is not None:
        error = True
    else:
        error = False

    CalcResults.update({'ExecutionTime': round(end_loop - start_loop, 5),
                        'warning': warning,
                        'error': error,
                        'error_message': error_message})

    res = make_response(jsonify(CalcResults), 200)

    return res


if __name__ == '__main__':

    ##############################################################
    ###################### Run the webapp ########################
    ##############################################################

    app.run(debug=True)


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
