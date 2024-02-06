from flask import Flask, jsonify, send_from_directory, url_for
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from modules.module import db, Car
import os

app = Flask(__name__)
CORS(app)
api = Api(app)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
# Определите путь к базе данных в том же каталоге, что и api.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'site.db')

db.init_app(app)

migrate = Migrate(app, db)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def save_uploaded_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return filename
    return ''

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
        parser.add_argument('photo', type=FileStorage, location='files')

        args = parser.parse_args()

        car = Car(
            brand=args['brand'],
            model=args['model'],
            year=args['year'],
            price=args['price'],
            color=args['color'],
            weight=args['weight'],
            mileage=args['mileage'],
            specs=args['specs'],
            photo=url_for('uploaded_file', filename=save_uploaded_file(args['photo']))
        )

        db.session.add(car)
        db.session.commit()

        return {'message': 'Added car'}, 201


api.add_resource(CarsResource, '/cars')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, ssl_context='adhoc', use_reloader=False)