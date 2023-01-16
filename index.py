from flask import Flask, request, render_template, send_from_directory, session, redirect
from  flask_session import Session
import os
import spotipy

REDIRECT_URL = 'http://127.0.0.1:5000/auth'
CLIENT_ID = "***REMOVED***"
CLIENT_SECRET = "***REMOVED***"
# python3 -m venv .venv
# source .venv/bin/activate
app = Flask(__name__)




app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)


# Debug setting set to true
app.debug = True



@app.route('/')
def index():
    # cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    # auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID,
    #                                            client_secret=CLIENT_SECRET,
    #                                            redirect_uri=REDIRECT_URL,
    #                                            scope='playlist-modify-private',
    #                                            cache_handler=cache_handler,
    #                                            show_dialog=True)
    return app.send_static_file('index.html')
    

@app.route('/login')
def login():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URL,
                                               scope='playlist-modify-private',
                                               cache_handler=cache_handler)
    auth_url = auth_manager.get_authorize_url()

    session["date"] = request.args.get("date")

    return render_template('login.html', auth_url=auth_url)
        




@app.route('/get/')
def get():
    return session.get('key', 'not set')


# @app.route('/start')
# def start():
    # :80 for http, :443 for https
    # URL: http://127.0.0.1:5000/start?parametr1=dupa&parametr2=blabla
    # parametr1 = request.args.get("parametr1")
    # parametr2 = request.args.get("parametr2")
    # return "parametr1 is " + parametr1 + " and parametr2 is " + parametr2


# res.redirect('https://accounts.spotify.com/authorize?' +
#     querystring.stringify({
#       response_type: 'code',
#       client_id: client_id,
#       scope: scope,
#       redirect_uri: redirect_uri,
#       state: state
#     }));

# 



@app.route('/auth')
def auth():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URL,
                                               scope='playlist-modify-private',
                                               cache_handler=cache_handler)
    auth_manager.get_access_token(request.args.get("code"))

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/login')

    return redirect('/playlist')
    # receive code
    # exchange code for token
    # read date from front-end

@app.route('/playlist')
def playlist():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URL,
                                               scope='playlist-modify-private',
                                               cache_handler=cache_handler)

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/login')

    date_now = session.get('date', None)

    return "hello" + date_now
    
    # run magic
    # serve done.html
    # handle errors
    

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)



if __name__ == '__main__':
    app.run()