from functools import wraps

from authlib.flask.client import OAuth
from six.moves.urllib.parse import urlencode
from flask import session, redirect

class Auth0Tool:
    class Config:
        CLIENT_ID = "client_id"
        CLIENT_SECRET = "client_secret"
        API_BASE_URL = "api_base_url"
        SCOPE = "scope"

    @classmethod
    def j_config2client_id(cls, j_config):
        return j_config[cls.Config.CLIENT_ID]

    @classmethod
    def j_config2client_secret(cls, j_config):
        return j_config[cls.Config.CLIENT_SECRET]

    @classmethod
    def j_config2api_base_url(cls, j_config):
        return j_config[cls.Config.API_BASE_URL]

    @classmethod
    def j_config2scope(cls, j_config):
        return j_config[cls.Config.SCOPE]


    @classmethod
    def app_config2auth0(cls, app, j_config):
        oauth = OAuth(app)

        base_url = cls.j_config2api_base_url(j_config)
        scope = cls.j_config2scope(j_config)
        access_token_url = "{}/oauth/token".format(base_url)
        authorize_url = "{}/authorize".format(base_url)

        auth0 = oauth.register(
            'auth0',
            client_id=cls.j_config2client_id(j_config),
            client_secret=cls.j_config2client_secret(j_config),
            api_base_url=base_url,
            access_token_url=access_token_url,
            authorize_url=authorize_url,
            client_kwargs={
                'scope': scope, #'openid profile email',
            },
        )
        return auth0

    @classmethod
    # Here we're using the /callback route.
    # @app.route('/callback')
    def auth0_url2callback(cls, auth0, url_redirect):
        # Handles response from token endpoint
        auth0.authorize_access_token()
        resp = auth0.get('userinfo')
        userinfo = resp.json()

        # Store the user information in flask session.
        session['jwt_payload'] = userinfo
        session['profile'] = {
            'user_id': userinfo['sub'],
            'name': userinfo['name'],
            'picture': userinfo['picture']
        }

        # return redirect('/dashboard')
        return redirect(url_redirect)

    @classmethod
    # @app.route('/login')
    def auth0_callback_url2login(cls, auth0, callback_url):
        return auth0.authorize_redirect(redirect_uri=callback_url)


    @classmethod
    def requires_auth(cls, func=None, login_url=None):
        if login_url is None:
            login_url = "/"

        def wrapper(f):
            @wraps(f)
            def wrapped(*_, **__):
                if 'profile' not in session:
                    # Redirect to Login page here
                    return redirect(login_url)
                return f(*_, **__)

            return wrapped

        return wrapper(func) if func else wrapper

    # @classmethod
    # @app.route('/dashboard')
    # @requires_auth
    # def dashboard():
    #     return render_template('dashboard.html',
    #                            userinfo=session['profile'],
    #                            userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))