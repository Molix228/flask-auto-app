from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
CORS(app)
api = Api(app)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

cars = []


class CarsResource(Resource):
    def get(self):
        return jsonify({'cars': cars})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('brand', type=str, required=True)
        parser.add_argument('model', type=str, required=True)
        parser.add_argument('year', type=int, required=True)
        parser.add_argument('price', type=float, required=True)
        parser.add_argument('color', type=str)
        parser.add_argument('weight', type=float)
        parser.add_argument('mileage', type=float)
        parser.add_argument('specs', type=str)
        parser.add_argument('photo', type=request.files.get)

        args = parser.parse_args()

        car = {
            'brand': args['brand'],
            'model': args['model'],
            'year': args['year'],
            'price': args['price'],
            'color': args['color'],
            'weight': args['weight'],
            'mileage': args['mileage'],
            'specs': args['specs'],
            'photo': save_uploaded_file(args['photo']),
        }

        cars.append(car)

        return {'message': 'Added car'}, 201


def save_uploaded_file(file):
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join('uploads', filename))
        return filename
    return ''


api.add_resource(CarsResource, '/api/cars')

# Маршрут для обслуживания статических файлов
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True, ssl_context='adhoc')