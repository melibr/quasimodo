from urllib.parse import urlencode
import json
import requests

AUTHORIZATION_ENDPOINT = 'http://auth.mercadolibre.com/authorization'
AUTHENTICATION_ENDPOINT= 'https://api.mercadolibre.com/oauth/token'

HEADERS = {'Accept': 'application/json', 'Content-type': 'application/json'}


class AuthConf:
    def __init__(self, app_id, secret_key):
        self.app_id = app_id
        self.secret_key = secret_key


class AuthURL:
    def __init__(self, auth_conf, response_type='code', endpoint=AUTHORIZATION_ENDPOINT):
        self.auth_conf = auth_conf
        self.endpoint = endpoint
        self.response_type = response_type

    def __repr__(self):
        self.params = {'client_id': self.auth_conf.app_id, 'response_type': self.response_type}
        self.url = '{}?{}'.format(self.endpoint, urlencode(self.params))

        return self.url


class AuthorizationCode:
    def __init__(self, auth_conf, code, redirect_uri, endpoint=AUTHENTICATION_ENDPOINT):
        self.auth_conf = auth_conf
        self.code = code
        self.redirect_uri = redirect_uri
        self.endpoint = endpoint

    @property
    def credentials(self):
        params = {'grant_type': 'authorization_code',
                  'code': self.code,
                  'client_id': self.auth_conf.app_id,
                  'client_secret': self.auth_conf.secret_key,
                  'redirect_uri': self.redirect_uri}

        self.r = requests.post(self.endpoint,
                                      params=urlencode(params), headers=HEADERS)

        if self.r.status_code == 200:
            return json.loads(self.r.text)


class RefreshToken:
    def __init__(self, auth_conf, refresh_token, endpoint=AUTHENTICATION_ENDPOINT):
        self.auth_conf = auth_conf
        self.refresh_token = refresh_token
        self.endpoint = endpoint

    @property
    def credentials(self):
        params = {'grant_type': 'refresh_token',
                  'refresh_token': self.refresh_token,
                  'client_id': self.auth_conf.app_id,
                  'client_secret': self.auth_conf.secret_key}

        self.r = requests.post(self.endpoint,
                                      params=urlencode(params), headers=HEADERS)

        if self.r.status_code == 200:
            return json.loads(self.r.text)
