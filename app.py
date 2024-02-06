from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    # Добавьте другие поля пользователя по необходимости

# Модель автомобиля
class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    color = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.Float)
    mileage = db.Column(db.Float)
    specs = db.Column(db.String(255))
    photo = db.Column(db.String(255))  # Путь к фото

    # Внешний ключ для связи с пользователем
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='cars')

# Создание всех таблиц в базе данных
db.create_all()

# Роут для получения всех автомобилей пользователя по его ID
@app.route('/api/users/<int:user_id>/cars', methods=['GET'])
def get_user_cars(user_id):
    user = User.query.get_or_404(user_id)
    cars = Car.query.filter_by(user=user).all()
    car_list = []
    for car in cars:
        car_list.append({
            'id': car.id,
            'brand': car.brand,
            'model': car.model,
            'type': car.type,
            'year': car.year,
            'price': car.price,
            'color': car.color,
            'weight': car.weight,
            'mileage': car.mileage,
            'specs': car.specs,
            'photo': car.photo
        })
    return jsonify({'cars': car_list})

if __name__ == '__main__':
    app.run(debug=True)