from flask import Flask, request, jsonify
from fastavro import writer, parse_schema
import os
import json

app = Flask(__name__)

# Define your Avro schema based on the provided JSON data
schema = {
    'doc': 'A record of a single sale',
    'name': 'Sale',
    'namespace': 'com.example.sales',
    'type': 'record',
    'fields': [
        {'name': 'client', 'type': 'string'},
        {'name': 'purchase_date', 'type': 'string'},  # Assuming ISO8601 date format.
        {'name': 'product', 'type': 'string'},
        {'name': 'price', 'type': 'float'}  # Use 'double' for higher precision if needed
    ]
}

def convert_json_to_avro(json_file_path: str, avro_file_path: str, schema: dict) -> None:
    # Read the JSON data
    with open(json_file_path, 'r') as f:
        data = json.load(f)  # This should be a list of records

    # Define Avro schema
    parsed_schema = parse_schema(schema)

    # Write the data to an Avro file
    with open(avro_file_path, 'wb') as out:
        writer(out, parsed_schema, data)

@app.route('/convert-to-avro', methods=['POST'])
def convert_to_avro_route():
    content = request.json
    raw_dir = content['raw_dir']
    stg_dir = content['stg_dir']
    # Ensure the storage directory exists
    os.makedirs(stg_dir, exist_ok=True)

    # Walk through the raw_dir to find all JSON files
    for subdir, dirs, files in os.walk(raw_dir):
        for json_filename in files:
            if json_filename.endswith('.json'):
                json_file_path = os.path.join(subdir, json_filename)
                relative_path = os.path.relpath(subdir, raw_dir)
                avro_subdir = os.path.join(stg_dir, relative_path)
                os.makedirs(avro_subdir, exist_ok=True)
                avro_filename = json_filename.replace('.json', '.avro')
                avro_file_path = os.path.join(avro_subdir, avro_filename)
                convert_json_to_avro(json_file_path, avro_file_path, schema)

    return jsonify({"status": "success", "message": "Data converted to Avro format successfully."})

if __name__ == '__main__':
    app.run(port=8082)
