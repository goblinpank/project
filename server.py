import random

from flask import Flask, render_template, jsonify, url_for, make_response, redirect, request, session
import datetime

from flask_login import login_manager, login_user, current_user

from data_1 import db_session
from data_1.weapons import Weapons
from data_1.users import User
from forms.LoginForm import LoginForm
import time

from forms.user import RegisterForm
from flask_login import LoginManager, login_user, login_required, logout_user

from flask_restful import reqparse, abort, Api, Resource
import glob
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def main():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    goblins = [
        {
            'image': 'characters/image1.png',  # путь относительно папки static/
            'name': 'Гоблин-Бомж',
            'price': 99,
            "link": "goblin_beggar"
        },
        {
            'image': 'characters/image2.png',
            'name': 'Гоблин-Шахтер',
            'price': 299,
            "link": "goblin_miner"
        },
        {
            'image': 'characters/image3.png',
            'name': 'Гоблин-Купец',
            'price': 599,
            "link": "goblin_seller"
        },
        {
            'image': 'characters/image4.png',
            'name': 'Гоблин-Царь',
            'price': 9999,
            "link": "goblin_king"
        }
    ]
    return render_template('main.html', goblins=goblins)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def sozdanie():
    user = User()
    user.name = "goblin_pank"
    user.set_password("123456")
    user.balance = 1000
    user.inventory = "1, 3, 17"
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == form.name.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.name == form.name.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            balance=1000,
            inventory=""
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)




@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")

parser = reqparse.RequestParser()
parser.add_argument('name', required=True)

class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('name', "balance", "inventory"))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        user = session.query(User).all()
        return jsonify({'user': [item.to_dict(
            only=('name', "balance", "inventory")) for item in user]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            name=args['name'],
        )
        session.add(user)
        session.commit()
        return jsonify({'id': user.id})

@app.route('/goblin_beggar')
def goblin_beggar():
    session = db_session.create_session()
    user = session.query(User).all()
    session = db_session.create_session()
    weapon = session.query(Weapons).filter(Weapons.name == 'авп драгон лор').first()
    return render_template('goblin_beggar.html', user=user, weapon=weapon)



@app.route('/get_random_image_beggar')
def get_random_image_beggar():
    # Выбираем случайную картинку
    images = [
        'characters/donk.jpg',
        'characters/tec_9.jpg',
        'characters/glock_18.jpg',
        "characters/tec_9.jpg",
        "characters/glock_18.jpg",
        "characters/tec_9.jpg",
        "characters/glock_18.jpg",
        "characters/tec_9.jpg",
        "characters/glock_18.jpg",
        "characters/tec_9.jpg",
        "characters/zeus.jpg",
        'characters/axia.jpg',
        'characters/agent.jpg',
        'characters/azimov.jpg',
        'characters/donk.jpg',
        'characters/tec_9.jpg',
        'characters/glock_18.jpg',
        "characters/tec_9.jpg",
        "characters/glock_18.jpg",
        'characters/sun_lion.jpg',
        'characters/sun_lion.jpg',
    ]
    image = random.choice(images)
    session = db_session.create_session()
    weapon = session.query(Weapons).filter(Weapons.picture == image).first()
    return jsonify({'image_url': url_for('static', filename=image),
                    "weapon": weapon.price,
                   "id":weapon.id})


@app.route('/goblin_miner')
def goblin_miner():
    session = db_session.create_session()
    user = session.query(User).all()
    session = db_session.create_session()
    weapon = session.query(Weapons).filter(Weapons.name == 'авп драгон лор').first()
    return render_template('goblin_miner.html', user=user, weapon=weapon)


@app.route('/get_random_image_miner')
def get_random_image_miner():
    # Выбираем случайную картинку
    images = [
        'characters/donk.jpg',
        'characters/tec_9.jpg',
        'characters/glock_18.jpg',
        'characters/zeus.jpg',
        "characters/glock_18.jpg",
        "characters/tec_9.jpg",
        "characters/glock_18.jpg",
        "characters/agent.jpg",
        'characters/donk.jpg',
        'characters/neonuar.jpg',
        'characters/neonuar.jpg',
        'characters/neonuar.jpg',
        "characters/axia.jpg",
        "characters/axia.jpg",
        'characters/paracord.jpg',
        'characters/usp.jpg',
        'characters/donk.jpg',
        'characters/donk.jpg',
        'characters/donk.jpg',
        "characters/agent.jpg",
        'characters/sun_lion.jpg',
        'characters/sun_lion.jpg',
        'characters/sun_lion.jpg',
    ]
    image = random.choice(images)
    session = db_session.create_session()
    weapon = session.query(Weapons).filter(Weapons.picture == image).first()
    return jsonify({'image_url': url_for('static', filename=image),
                    "weapon": weapon.price,
                   "id":weapon.id})

@app.route('/goblin_seller')
def goblin_seller():
    session = db_session.create_session()
    user = session.query(User).all()
    session = db_session.create_session()
    weapon = session.query(Weapons).filter(Weapons.name == 'авп драгон лор').first()
    return render_template('goblin_seller.html', user=user, weapon=weapon)


@app.route('/get_random_image_seller')
def get_random_image_seller():
    # Выбираем случайную картинку
    images = [
        'characters/donk.jpg',
        'characters/tec_9.jpg',
        'characters/glock_18.jpg',
        'characters/zeus.jpg',
        "characters/glock_18.jpg",
        "characters/tec_9.jpg",
        "characters/glock_18.jpg",
        "characters/agent.jpg",
        'characters/donk.jpg',
        'characters/neonuar.jpg',
        'characters/neonuar.jpg',
        'characters/neonuar.jpg',
        'characters/neonuar.jpg',
        'characters/neonuar.jpg',
        'characters/axia.jpg',
        'characters/axia.jpg',
        'characters/vape.jpg,',
        'characters/vape.jpg',
        'characters/usp.jpg',
        'characters/survival.jpg',
        'characters/paracord.jpg',
        'characters/azimov.jpg',
        'characters/sun_lion.jpg',
        'characters/sun_lion.jpg',
    ]
    image = random.choice(images)
    session = db_session.create_session()
    weapon = session.query(Weapons).filter(Weapons.picture == image).first()
    return jsonify({'image_url': url_for('static', filename=image),
                    "weapon": weapon.price,
                   "id": weapon.id})


@app.route('/goblin_king')
def goblin_king():
    session = db_session.create_session()
    user = session.query(User).all()
    session = db_session.create_session()
    weapon = session.query(Weapons).filter(Weapons.name == 'авп драгон лор').first()
    return render_template('goblin_king.html', user=user, weapon=weapon)


@app.route('/get_random_image_king')
def get_random_image_king():
    # Выбираем случайную картинку
    images = [
        'characters/skeleton.jpg',
        'characters/kogot.jpg',
        'characters/survival.jpg',
        'characters/paracord.jpg',
        'characters/m9_knife.jpg',
        'characters/howl.jpg',
        'characters/butterfly_knife.jpg',
        'characters/dragon_lore.jpg',
        'characters/donk.jpg',
        'characters/survival.jpg',
        'characters/paracord.jpg',
        'characters/survival.jpg',
        'characters/paracord.jpg',
        'characters/skeleton.jpg',
        'characters/kogot.jpg',
        'characters/paracord.jpg',
        'characters/paracord.jpg',
        'characters/paracord.jpg',

    ]
    image = random.choice(images)
    session = db_session.create_session()
    weapon = session.query(Weapons).filter(Weapons.picture == image).first()
    return jsonify({'image_url': url_for('static', filename=image),
                    "weapon": weapon.price,
                   "id":weapon.id})



@app.route('/deduct_balance', methods=['POST'])
@login_required
def deduct_balance():
    session = db_session.create_session()
    user = session.query(User).filter(User.name == current_user.name).first()
    data = request.get_json()
    amount = data.get('amount')
    if user.balance >= amount:
        user.balance -= amount
        session.commit()
        return jsonify({'success': True, 'balance': user.balance})
    else:
        return jsonify({'success': False, 'error': 'Недостаточно средств'}), 400

@app.route('/sell', methods=['POST'])
@login_required
def sell():
    session = db_session.create_session()
    user = session.query(User).filter(User.name == current_user.name).first()
    data = request.get_json()
    amount = data.get('amount')
    user.balance += amount
    session.commit()
    return jsonify({'success': True, 'balance': user.balance})


@app.route('/add_item', methods=['POST'])
@login_required
def add_item():
    session = db_session.create_session()
    user = session.query(User).filter(User.name == current_user.name).first()
    data = request.get_json()
    item = data.get('id')
    if user.inventory:
        user.inventory += f", {item}"
    else:
        user.inventory = f"{item}"
    session.commit()
    return jsonify({'success': True, 'inventory': user.inventory})

@app.route("/profile")
def profile():
    session = db_session.create_session()
    user = session.query(User).filter(User.name == current_user.name).first()
    weapon = session.query(Weapons).all()
    weapon_list = [
        {"id": i.id, "price": i.price} for i in weapon
    ]
    if user.inventory:
        user_inventory_ids = [int(i) for i in user.inventory.split(", ")]
    else:
        user_inventory_ids = []
    return render_template('profile.html', user=user, weapon=weapon,
                           weapon_list=weapon_list, user_inventory=user_inventory_ids)


@app.route('/sell_all', methods=['POST'])
def sell_all():
    data = request.get_json()
    total_sale = data.get('totalSale')

    # Проверка
    if total_sale is None:

        return jsonify({'success': False, 'message': 'Нет данных о продаже'})

    try:
        total_sale = float(total_sale)

    except (TypeError, ValueError) as e:
        return jsonify({'success': False, 'message': 'Некорректное значение totalSale'})

    # Получаем пользователя
    session = db_session.create_session()
    user = session.query(User).filter(User.id == current_user.id).first()
    if not user:
        return jsonify({'success': False, 'message': 'Пользователь не найден'})

    # Обновляем баланс
    user.balance += total_sale
    user.inventory = ""

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        return jsonify({'success': False, 'message': 'Ошибка при сохранении данных'})

    from flask_login import login_user
    login_user(user)

    return jsonify({'success': True, 'balance': user.balance})

if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')

