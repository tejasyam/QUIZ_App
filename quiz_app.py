from app import application
from app.apis import *
from app.models import db


if __name__ == '__main__':
    with application.app_context():
        db.create_all()

    application.run(debug=True, port=8000)