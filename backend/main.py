from flask import request, jsonify,session,redirect
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from config import app, db,jwt,spotify_creds
import os
import bcrypt
import requests
import base64
from urllib.parse import urlencode
import SpotifyInterface

@app.route('/login')
def login():
    auth_url = (
        "https://accounts.spotify.com/authorize"
        "?response_type=code"
        f"&client_id={spotify_creds['client_id']}"
        f"&scope={spotify_creds['scope']}"
        f"&redirect_uri={spotify_creds['backend_redirect_uri']}"
    )
    return redirect(auth_url)


@app.route('/callback')
def callback():
    code = request.args.get('code')
    auth_str = f"{spotify_creds["client_id"]}:{spotify_creds["client_secret"]}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    response = requests.post("https://accounts.spotify.com/api/token", data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': spotify_creds['backend_redirect_uri']
    }, headers={
        'Authorization': f'Basic {b64_auth_str}',
        'Content-Type': 'application/x-www-form-urlencoded'
    })

    tokens = response.json()
    access_token = tokens.get('access_token')
    refresh_token = tokens.get('refresh_token')

    # Store tokens in session, DB, or return to frontend
    query_params = urlencode({
        "access_token": access_token,
        "refresh_token": refresh_token
    })

    return redirect(f"{spotify_creds['frontend_redirect_uri']}?{query_params}")

@app.route('/create_playlist',methods=['POST'])
def create_playlist():
    try:
        data = request.get_json()
        
        instance = SpotifyInterface.SpotifyInterface(data.get('access_token'),data.get("refresh_token"))
        genres = instance.get_genres(data.get("prompt"))

        ret = SpotifyInterface.create_mixed_playlist(data.get("access_token"),genres,data.get("prompt"))

        return jsonify({"data":ret})
    except Exception as e:
        print(e)
        return 400

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0',port=5000,debug=True)