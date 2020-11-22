from flask import Flask
from environs import Env
import firebase_admin
from firebase_admin import credentials, firestore
from uwsgidecorators import *
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

# Load firebase credentials
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
fb = firestore.client()

limiter = 0


@timer(1800)
def updateStatus(signum):
    """
    Updates firebase once every 30 minutes.
    :param signum: Signum needed by firebase.
    """
    print("Status updated.")
    ref = fb.collection(u'api').document(u'j087hhlFv3IHzcz89OAZ')
    ref.update({
        u'api_online': 1,
        u'last_online': firestore.SERVER_TIMESTAMP
    })


def create_api():
    """
    This function sets up the API based on configurations
    :return: app
    """

    app = Flask(__name__, root_path=os.path.abspath('.'))
    app.config['UPLOAD_FOLDER'] = '../static'
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

    global limiter
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["50 per day", "10 per hour"]
    )

    env = Env()
    env.read_env('.env')

    # Register Blueprints
    from src.routes.open import open_routes
    app.register_blueprint(open_routes, url_prefix='/')

    return app
