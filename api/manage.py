import os

from flask_script import Manager

from app import create_app


def init_manager():
    config_name = os.environ.get("APP_SETTINGS", "development")
    app = create_app(config_name)
    manager = Manager(app)
    manager.run()


if __name__ == "__main__":
    init_manager()
