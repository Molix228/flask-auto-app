from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

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
        'brand': data['brand'],
        'model': data['model'],
        'year': data['year'],
        'price': data['price'],
        'color': data['color'],
        'weight': data['weight'],
        'mileage': data['mileage'],
        'specs': data['specs'],
        'photo': data.get('photo', ''),
    }

    cars.append(car)

    return jsonify({'message': 'Added car'}), 201

@app.route('/api/cars', methods=["GET"])
def get_cars():
    return jsonify({'cars': cars})

# Маршрут для обслуживания статических файлов
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)