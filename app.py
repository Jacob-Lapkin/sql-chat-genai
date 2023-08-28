from flask import Flask, request, jsonify
from create_app import create_app
from dotenv import load_dotenv
import os

environment = os.getenv('FLASK_ENV', 'development')

app = create_app(environment)

debug_mode = app.config["DEBUG"]

if __name__ == "__main__":
    app.run(debug=debug_mode, port=5000, host='0.0.0.0')
