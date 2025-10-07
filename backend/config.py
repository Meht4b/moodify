from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from sqlalchemy import event
from sqlalchemy.engine import Engine
import os 
from dotenv import load_dotenv

load_dotenv()
jwt_secret_key = os.getenv('JWT_SECRET_KEY')
client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
backend_redirect_uri = os.getenv('BACKEND_REDIRECT_URI')
frontend_redirect_uri = os.getenv('FRONTEND_REDIRECT_URI')
scope = (
    "user-read-playback-state "
    "user-modify-playback-state "
    "playlist-modify-public "
    "user-library-read "
    "user-library-modify "
    "playlist-modify-private "
    "playlist-read-collaborative "
    "playlist-read-private "
    "user-read-currently-playing "
    "user-read-recently-played"
)


spotify_creds = {
    "client_id": client_id,
    "client_secret": client_secret,
    "backend_redirect_uri": backend_redirect_uri,
    "frontend_redirect_uri": frontend_redirect_uri,
    "scope": scope
}

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = jwt_secret_key




jwt = JWTManager(app)

CORS(app)

db = SQLAlchemy(app)