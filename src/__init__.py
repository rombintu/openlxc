from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager
# from .config import DATABASE

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret123'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # следующие две строчки для свича бд, если нужна postgres, расскомментить
    # app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://test:password@localhost:5432/gamix"
    # app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
    


    # login_manager = LoginManager()
    # login_manager.login_view = 'auth.login'
    # login_manager.init_app(app)

    # # Импорт модели юзера для отслеживания входа в систему
    # from .model import Users


    # # Подключение blueprint
    # from .auth import auth as auth_blueprint
    # app.register_blueprint(auth_blueprint)

    # from .main import main as main_blueprint
    # app.register_blueprint(main_blueprint)
    
    # @login_manager.user_loader
    # def load_user(user_id):
    #     engine = create_engine(DATABASE)
    #     Session = sessionmaker(bind=engine)
    #     session = Session()
    #     user = session.query(Users).filter(Users.id == int(user_id)).first()
    #     session.close()
    #     return user
    return app