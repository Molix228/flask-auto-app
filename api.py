# app.py
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse
from werkzeug.utils import secure_filename
from modules.module import db, Car

app = Flask(__name__)
CORS(app)
api = Api(app)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Используйте свою базу данных

db.init_app(app)

# ...

class CarsResource(Resource):
    def get(self):
        cars = Car.query.all()
        return jsonify({'cars': [{'brand': car.brand, 'model': car.model, 'year': car.year, 'price': car.price,
                                  'color': car.color, 'weight': car.weight, 'mileage': car.mileage, 'specs': car.specs,
                                  'photo': car.photo} for car in cars]})

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

        car = Car(brand=args['brand'], model=args['model'], year=args['year'], price=args['price'],
                  color=args['color'], weight=args['weight'], mileage=args['mileage'], specs=args['specs'],
                  photo=save_uploaded_file(args['photo']))

        db.session.add(car)
        db.session.commit()

        return {'message': 'Added car'}, 201

# ...

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, ssl_context='adhoc')
