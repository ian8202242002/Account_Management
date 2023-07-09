from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from apis import blueprint
from database import db


def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    db.init_app(app)
    app.register_blueprint(blueprint)
    return app

def setup_database(app):
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    app = create_app()
    setup_database(app)
    app.run(debug=True, host='0.0.0.0', port=8888)
