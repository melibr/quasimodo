from urllib.parse import urlencode
import json
import requests

AUTHORIZATION_URL = 'http://auth.mercadolibre.com/authorization'
AUTHENTICATION_URL = 'https://api.mercadolibre.com/oauth/token'


class AuthConf:
    def __init__(self, app_id, secret_key):
        self.app_id = app_id
        self.secret_key = secret_key


class AuthURL:
    def __init__(self, auth_conf, redirect_uri=None,
                 response_code='code', auth_url=AUTHORIZATION_URL):
        self.auth_conf = auth_conf
        self.auth_url = auth_url
        self.redirect_uri = redirect_uri
        self.response_code = response_code

    def __repr__(self):
        self.params = {'client_id': self.auth_conf.app_id, 'response_type': self.response_code}

        if self.redirect_uri:
            self.params.update({'redirect_uri': self.redirect_uri})

        params = urlencode(self.params)

        self.url = '{}?{}'.format(self.auth_url, params)

        return self.url


class AuthorizationCode:
    headers = {'Accept': 'application/json', 'Content-type': 'application/json'}

    def __init__(self, auth_conf, code, redirect_uri, auth_url=AUTHENTICATION_URL):
        self.auth_conf = auth_conf
        self.code = code
        self.redirect_uri = redirect_uri
        self.auth_url = auth_url

    @property
    def credentials(self):
        params = {'grant_type': 'authorization_code',
                  'code': self.code,
                  'client_id': self.auth_conf.app_id,
                  'client_secret': self.auth_conf.secret_key,
                  'redirect_uri': self.redirect_uri}

        self.r = requests.post(self.auth_url,
                                      params=urlencode(params), headers=self.headers)

        if self.r.status_code == 200:
            return json.loads(self.r.text)

        return {}
