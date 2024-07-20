from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
import os
import utils
from datetime import datetime

app = Flask(__name__)
load_dotenv()

expected_password = os.getenv('PASSWORD')
keys_filepath = os.getenv('KEYS_FILEPATH')
log_filepath = os.getenv('LOG_FILEPATH')
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/vps-logins',methods=['POST'])
def protected():
    password=request.json.get("password")
    if password==expected_password:
        sessions=utils.process_sessions(keys_filepath, log_filepath)
        return (sessions), 200
    return {"message":"password error"}, 401


if __name__ == '__main__':
    app.run(debug=True)
