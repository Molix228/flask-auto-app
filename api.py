import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Указываем директорию для статических файлов (например, изображений)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

cars = []


@app.route('/api/cars', methods=["POST"])
def add_car():
    data = request.form  # Используем request.form для данных формы

    if 'brand' not in data or 'model' not in data:
        return jsonify({'error': 'Missing brand/model'}), 400

    car = {
        'brand': data.get('brand'),
        'model': data.get('model'),
        'year': int(data.get('year')),
        'price': float(data.get('price')),
        'color': data.get('color'),
        'weight': float(data.get('weight')),
        'mileage': float(data.get('mileage')),
        'specs': data.get('specs'),
        'photo': save_uploaded_file(request.files.get('photo')),  # Save and store filename
    }

    cars.append(car)

    response = jsonify({'message': 'Added car'})

    return response, 201

def save_uploaded_file(file):
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join('uploads', filename))
        return filename
    return ''

@app.route('/api/cars', methods=["GET"])
def get_cars():
    return jsonify({'cars': cars})

# Маршрут для обслуживания статических файлов
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True, ssl_context='adhoc')  # Запуск через HTTPS
