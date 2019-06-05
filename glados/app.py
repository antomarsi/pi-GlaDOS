from flask import Flask
from flask_restplus import Resource, Api
from api1 import blueprint as api1

app = Flask(__name__)

app.register_blueprint(api1, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)