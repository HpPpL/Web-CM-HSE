from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
import os
import shutil
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from checker import Test

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

# Определение модели пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Проверка пароля
@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return username

@app.route('/upload', methods=['POST'])
@auth.login_required
def upload_file():
    response = {'success': False, 'message': ''}
    file = request.files['file']

    if file.filename == '':
        response['message'] = 'Файл не выбран'
        return jsonify(response)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join('temp-data', filename)
        file.save(file_path)

        tester = Test()
        valid, message = tester.validate(file_path)
        if valid:
            new_name = 'data' + os.path.splitext(filename)[1]
            new_file_path = os.path.join('test-real-data', new_name)
            shutil.copy(file_path, new_file_path)

            response['success'] = True
            response['message'] = 'Файл успешно загружен и проверен'
        else:
            os.remove(file_path)
            response['message'] = message
        return jsonify(response)
    else:
        response['message'] = 'Файл не подходит по формату'
        return jsonify(response)

@app.route('/', methods=['GET'])
@auth.login_required
def index():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'xlsx', 'xls'}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создание таблиц, если они еще не созданы
    app.run(host='0.0.0.0', port=5000)

