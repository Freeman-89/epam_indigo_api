from flask import Flask
from lib.routes import api, swagger_ui_blueprint
from lib.utils import FileHendler
from flask_cors import CORS
import threading
import time


file_hendler = FileHendler(dir='/app/static/tmp')
def cleanup_loop():
    while True:
        file_hendler.mayby_cleanupup(max_age_sec=60)
        time.sleep(30)

threading.Thread(target=cleanup_loop, daemon=True).start()


app = Flask(__name__, static_url_path='/static', static_folder='static')
app.register_blueprint(swagger_ui_blueprint, url_prefix='/api/swagger')
app.register_blueprint(api, url_prefix="/api")
CORS(app)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)