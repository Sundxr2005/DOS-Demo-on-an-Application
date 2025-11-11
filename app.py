from flask import Flask, send_from_directory, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

app = Flask(__name__, static_folder='.', static_url_path='/')
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["10 per second;200 per minute"]
)
limiter.init_app(app)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    if os.path.exists(filename):
        return send_from_directory('.', filename)
    return "Not found", 404

@app.route('/ping')
@limiter.limit("5 per second")
def ping():
    return jsonify(status="ok"), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
# Correct way
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["10 per second", "200 per minute"]
)