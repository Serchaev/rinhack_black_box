import json

from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)


def load_data():
    with open('data1.json', 'r') as file:
        data = json.load(file)

    df = pd.DataFrame(data["data"], columns=data['columns'])
    return df, data["columns"]


@app.route('/', methods=['POST'])
def home():
    request_data = request.get_json()

    if 'id' in request_data:
        requested_id = request_data['id']

        loaded_data, data = load_data()
        found_object = loaded_data.loc[requested_id].to_dict()
        if found_object:
            return jsonify({"user": found_object, "data": data})
        else:
            result = {'error': f'Object with id {requested_id} not found.'}
            return jsonify(result), 404

    else:
        result = {'error': 'Invalid JSON format. Make sure to include "id" field.'}
        return jsonify(result), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=25564)
