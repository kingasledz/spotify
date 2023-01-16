from flask import Flask, request, render_template, send_from_directory

REDIRECT_URL = 'http://127.0.0.1:5000/auth'

app = Flask(__name__)

# Debug setting set to true
app.debug = True

@app.route('/')
def index():
    # serve index.html
    # return render_template('index.html')
    return app.send_static_file('index.html')

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
    # receive code
    # exchange code for token
    # read date from front-end
    return "hello world"

@app.route('/playlist')
def playlist():
    # run magic
    # serve done.html
    # handle errors
    pass

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)



if __name__ == '__main__':
    app.run()