from flask import Flask, request, jsonify
from typing import Dict, Any
import requests
import os
import shutil

app = Flask(__name__)

AUTH_TOKEN = os.environ.get('AUTH_TOKEN', 'your-default-token')


# Type hint for a function that accepts a string and returns None
def clean_directory(path: str) -> None:
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


# Type hint for a function that accepts strings for date and directory path, and returns None
def fetch_and_save_sales_data(date: str, raw_dir: str) -> None:
    page = 1
    while True:
        response = requests.get(
            url=f'https://fake-api-vycpfa6oca-uc.a.run.app/sales',
            params={'date': date, 'page': page},
            headers={'Authorization': AUTH_TOKEN}
        )

        if response.status_code != 200 or not response.json():
            break  # Stop if there's an error or no more data

        # File path construction with type hint for the file_name variable
        file_name: str = f'sales_{date}_{page}.json' if page > 1 else f'sales_{date}.json'
        file_path = os.path.join(raw_dir, file_name)

        # Writing data to file
        with open(file_path, 'w') as file:
            file.write(response.text)
        page += 1


# Type hint for a view function that returns a Flask Response object
@app.route('/fetch-sales', methods=['POST'])
def fetch_sales() -> Any:
    data: Dict[str, str] = request.json
    date: str = data.get('date')
    raw_dir: str = data.get('raw_dir')

    directory_path: str = os.path.join(raw_dir, 'sales', date)
    clean_directory(directory_path)
    fetch_and_save_sales_data(date, directory_path)

    return jsonify({"status": "success", "message": "Data fetched and saved successfully."}), 200


if __name__ == '__main__':
    app.run(port=8081)
