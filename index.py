from flask import Flask, request, render_template, send_from_directory, session, redirect
from  flask_session import Session
import os
import spotipy
import spo_create

REDIRECT_URL = "http://127.0.0.1:5000/auth"
CLIENT_ID = "***REMOVED***"
CLIENT_SECRET = "***REMOVED***"

app = Flask(__name__)




app.config["SECRET_KEY"] = os.urandom(64)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = "./.flask_session/"
Session(app)



app.debug = True



@app.route("/")
def index():
    return app.send_static_file("index.html")



@app.route("/login")
def login():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URL,
                                               scope="playlist-modify-private",
                                               cache_handler=cache_handler)
    auth_url = auth_manager.get_authorize_url()

    session["date"] = request.args.get("date")

    return render_template("login.html", auth_url=auth_url)
        

@app.route("/auth")
def auth():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URL,
                                               scope="playlist-modify-private",
                                               cache_handler=cache_handler)
    auth_manager.get_access_token(request.args.get("code"))

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect("/login")

    #return redirect("/playlist") 

    return render_template("waiting.html")


@app.route("/playlist")
def playlist():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URL,
                                               scope="playlist-modify-private",
                                               cache_handler=cache_handler)

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect("/login")
   
        

    date_now = session.get("date", None)

    try:
        playlist_link = spo_create.create_playlist(date_now,auth_manager)
        return render_template("playlist.html", playlist_link=playlist_link)
    except:
        return render_template("error.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("static", path)



if __name__ == "__main__":
    app.run()