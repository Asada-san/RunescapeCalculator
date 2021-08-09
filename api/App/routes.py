from api.App.PythonRevolution import Revolution_main as RevoMain
from api.App.models import Counter
from api.App import db
from api.AbilityBook import AbilityBook
from flask import url_for, render_template, request, Blueprint, redirect, send_from_directory
from flask import make_response, jsonify, send_file
from flask_cors import CORS
import os
import requests
from bs4 import BeautifulSoup
import json
import time
import random
import pprint


api = Blueprint('api', __name__)
CORS(api, resources={r"/api/*": {"origins": "*"}}, support_credentials=True)


def get_tradeable_itemIDs():
    item_list = {}
    number_of_categories = 42
    max_amount_of_pages = 20

    # For every category on the Grand Exchange catalogue page starting at 0
    for i in range(0, number_of_categories):
        end_loop = False
        time.sleep(10)

        # For every page in a given category (make sure the pages don't go over 20 offline) starting at 1
        for j in range(1, max_amount_of_pages + 1):
            # The url of category i and page j
            url = f"http://services.runescape.com/m=itemdb_rs/catalogue?cat={i}&page={j}"
            # Get the html code of the page

            # custom header cause Jagex... (noindex/nofollow)
            UAS = (
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
            "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
            )

            ua = UAS[random.randrange(len(UAS))]

            r = requests.get(url, headers={'user-agent': ua})

            # Clean that shit up
            soup = BeautifulSoup(r.text, 'html.parser')

            # Find all the table rows
            rows = soup.find('table').find('tbody').find_all('tr')

            for row in rows:
                # The item name and id are both in a img element within a table row
                img_element = row.find('td').find('a').find('img')
                item = img_element['title']
                # The id is buried a bit deeper within the source link of the image
                link = img_element['src']
                id = link.split('=')[-1]

                # Verify if all items in the category are checked
                if id in item_list:
                    end_loop = True
                    break
                else:
                    item_list.update({id: item})

            if end_loop:
                break
            else:
                time.sleep(3)

    # Save the list
    with open('api/App/itemIDs.json', 'w') as file:
        json.dump(item_list, file)

    return None


# get_tradeable_itemIDs()


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