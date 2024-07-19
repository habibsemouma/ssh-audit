from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
import os

app = Flask(__name__)
load_dotenv()

app.secret_key = os.getenv('SECRET_KEY')

password = os.getenv('PASSWORD')
CORS(app)


@app.route('/vps-logins')
def protected():
    return ([{"quantity":"qsdqsd"}]), 200


if __name__ == '__main__':
    app.run(debug=True)
