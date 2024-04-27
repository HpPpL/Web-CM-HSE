from web import app, db, User

username = input("Введите имя пользователя: ")
password = input("Введите пароль: ")

with app.app_context():
    if User.query.filter_by(username=username).first() is not None:
        print(f"Пользователь с именем {username} уже существует.")
    else:
        user = User(username=username)
        user.set_password(password)  # Пароль будет хеширован в этом методе
        db.session.add(user)
        db.session.commit()
        print(f"Пользователь {username} успешно создан.")
