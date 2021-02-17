import logging
from dataclasses import dataclass
from functools import wraps
from pprint import pformat
from typing import Optional

import requests
from authlib.integrations.flask_client import OAuth
from flask import session, redirect

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.network.requests.requests_tool import RequestsTool


class Auth0WebappTool:
    @dataclass
    class Config:
        client_id: str
        client_secret: str
        api_url_base: str
        scope: str
        audience: Optional[str]

    @classmethod
    def app_config2auth0(cls, app, config: Config):
        oauth = OAuth(app)

        base_url = config.api_url_base
        scope = config.scope
        access_token_url = "{}/oauth/token".format(base_url)
        authorize_url = "{}/authorize".format(base_url)

        auth0 = oauth.register(
            'auth0',
            client_id=config.client_id,
            client_secret=config.client_secret,
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
