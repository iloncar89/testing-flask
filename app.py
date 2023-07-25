from flask import Flask

from config import containers
from controller import testController


def create_app() -> Flask:
    container = containers.Container()
    db = container.dbORM()
    db.create_database()
    app = Flask(__name__)
    app.container = container
    app.register_blueprint(testController.blueprint, url_prefix="/api/v1/test")

    return app


app = create_app()
