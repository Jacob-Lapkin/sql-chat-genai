from flask import Flask, request, jsonify
import os
from flasgger import Swagger
from config.configuration import Development, Production
from api.routes import parent_bp
from api.utils.misc.swagger_docs import swagger_config
from flask_cors import CORS



def create_app(environment):
    app = Flask(__name__)

    swagger = Swagger(app, config=swagger_config)  # Initialize Flasgger

    CORS(app)

    if environment == "production":
        app.config.from_object(Production())
    else:
        app.config.from_object(Development())

    version = app.config['VERSION']
    hostname = app.config['HOSTNAME']

    app.register_blueprint(parent_bp, url_prefix=f'/{hostname}/{version}')

    @app.route('/home', methods=['GET'])
    def home():
        return jsonify({"response":"welcome to insights generator"}), 200
    return app
