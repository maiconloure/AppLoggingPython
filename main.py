from flask import Flask
from flask_restful import Api
from app.log_catcher.app import LogCatcher

app = Flask(__name__)
api = Api(app)

api.add_resource(LogCatcher, '/logger_catcher', '/logger_catcher')

if __name__ == '__main__':
    app.run(port=5555)