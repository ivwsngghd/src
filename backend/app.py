import os

import package
from dbs import Flask
from models import db
from utils import test


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DEBUG=True
    )
    # app.secret_key = os.environ.get('SECRET_KEY')
    app.secret_key = 'ivwsngghd23333333333333333'
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://ivwsngghd:8232470785@182.92.218.194:3306/assets?charset=utf8"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get(
        'SQLALCHEMY_TRACK_MODIFICATIONS', default=False)
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True  # 用于热加载
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    import auth
    import inventory
    app.register_blueprint(auth.bp)
    app.register_blueprint(inventory.bp)
    app.register_blueprint(package.bp)
    app.register_blueprint(test.bp)

    db.init_app(app)
    db.app = app
    db.create_all()
    return app
