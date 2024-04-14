from flask import Flask, request, jsonify
import requests
import os
import shutil

app = Flask(__name__)

AUTH_TOKEN = os.environ['AUTH_TOKEN']


# Функція для очищення директорії
def clean_directory(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


# Функція для зберігання даних з API
def fetch_and_save_sales_data(date, raw_dir):
    page = 1
    while True:
        response = requests.get(
            url=f'https://fake-api-vycpfa6oca-uc.a.run.app/sales',
            params={'date': date, 'page': page},
            headers={'Authorization': AUTH_TOKEN}
        )

        if response.status_code != 200 or not response.json():
            break  # Stop if there's an error or no more data

        # Шлях і ім'я файлу
        file_name = f'sales_{date}_{page}.json' if page > 1 else f'sales_{date}.json'
        file_path = os.path.join(raw_dir, file_name)

        # Запис даних в файл
        with open(file_path, 'w') as file:
            file.write(response.text)
        page += 1


# Маршрут для POST-запиту
@app.route('/fetch-sales', methods=['POST'])
def fetch_sales():
    data = request.json
    date = data.get('date')
    raw_dir = data.get('raw_dir')

    # Шлях до директорії
    directory_path = os.path.join(raw_dir, 'sales', date)

    # Очищення директорії перед записом нових файлів
    clean_directory(directory_path)

    # Виклик функції для витягування даних
    fetch_and_save_sales_data(date, directory_path)

    return jsonify({"status": "success", "message": "Data fetched and saved successfully."}), 200


if __name__ == '__main__':
    app.run(port=8081)
