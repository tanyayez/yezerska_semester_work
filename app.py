#це програма яка використовує GoogleAPI для реєстрації в додаток
from flask import Flask, render_template, request, redirect, url_for, session
from flask_oauth import OAuth
import json


USERNAME = None
FILENAME = None
app = Flask(__name__)


GOOGLE_CLIENT_ID = '359520140035-0nlqnjo2g2daujj0algii7m5fff21hif.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'p9MkeBPqw0lob_Tke1BZsX8N'
REDIRECT_URI = '/authorized'  # one of the Redirect URIs from Google APIs console
SECRET_KEY = 'development key'
app.secret_key = SECRET_KEY
oauth = OAuth()
google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
                                                'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=GOOGLE_CLIENT_ID,
                          consumer_secret=GOOGLE_CLIENT_SECRET)


def index():
    global USERNAME, FILENAME
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('login'))
    access_token = access_token[0]
    from urllib.request import Request, urlopen
    from urllib.error import URLError
    headers = {'Authorization': 'OAuth ' + access_token}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                  None, headers)
    try:
        res = urlopen(req)
    except URLError as e:
        if e.code == 401:
            # Unauthorized - bad token
            session.pop('access_token', None)
            return redirect(url_for('login'))
        return res.read()
    json_string = res.read().decode('utf-8')
    json_obj = json.loads(json_string)
    USERNAME = json_obj['name']
    FILENAME = json_obj['email'][:json_obj['email'].index('@')]
    FILENAME = str(FILENAME) + '.csv'
    return render_template('home.html')


@app.route('/')
def login():
    callback = url_for('authorized', _external=True)
    return google.authorize(callback=callback)


@app.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return index()


@google.tokengetter
def get_access_token():
    return session.get('access_token')


@app.route('/start')
def start():
    return render_template('welcome.html')

if __name__ == "__main__":
    app.run(debug = True)