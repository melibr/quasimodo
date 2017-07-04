import requests

from datetime import datetime
from urllib.parse import urlencode

from .auth import (AuthConf, AuthURL,
                  AuthorizationCode, RefreshToken)



TOKEN_SESSION_NAME = 'quasimodo_token'
AUTHORIZED_DATETIME_SESSION_NAME = 'quasimodo_authorized_datetime'
EXPIRES_IN_SESSION_NAME = 'quasimodo_expires_in'

API_URI = 'https://api.mercadolibre.com/{endpoint}';


class Quasimodo:
    def __init__(self, app_id=None, secret_key=None, session={}):
        self._auth_conf = AuthConf(app_id, secret_key)
        self._session = session
        self._token = None
        self._offset = 0
        self.paging = {}

    def get_auth_url(self):
        return AuthURL(self._auth_conf)

    def authorize(self, code, redirect_uri=None):
        authorization_code = AuthorizationCode(self._auth_conf, code, redirect_uri)
        return self.update_session(authorization_code)

    def refresh(self):
        refresh_token = RefreshToken(self._auth_conf, self.refresh_token)
        return self.update_session(refresh_token)

    def is_authenticated(self):
        return AUTHORIZED_DATETIME_SESSION_NAME in self._session

    def update_session(self, o):
        self._credentials = o.credentials
        self._session[TOKEN_SESSION_NAME] = self._credentials.get('access_token') or self._credentials.get('refresh_token')
        self._session[AUTHORIZED_DATETIME_SESSION_NAME] = datetime.now().isoformat()
        self._session[EXPIRES_IN_SESSION_NAME] = self._credentials.get('expires_in')

        return self._credentials

    def request(self, method, endpoint, params={}, **kwargs):
        params = {**{'access_token': self._token}, **params}
        qs = urlencode(params)
        return requests.request(method, API_URI.format(endpoint=endpoint + '?' + qs, access_token=self.token), **kwargs).json()

    def set_token(self, token):
        self._token = token
        return self._token

    def set_offset(self, offset):
        self._offset = offset
        return self._offset

    @property
    def token(self):
        return self._token or self._session.get(TOKEN_SESSION_NAME)

    @property
    def me(self):
        return self.request('GET', 'users/me')

    def set_offset(self, offset):
        self._offset = offset

    def get_products(self, params={}):
        user = self.me
        identifier = user.get('id')
        data = self.request('GET', 'users/{identifier}/items/search'.format(identifier=identifier), params)

        self.paging = data.get('paging', {})
        self.total = self.paging.get('total', 0)
        self.limit = self.paging.get('limit', 0)
        
        return data.get('results')

    def get_product_description(self, identifier):
        data = self.request('GET', 'items/{identifier}/description'.format(identifier=identifier))
        return data.get('text')

    def update_product_description(self, identifier, description):
        self.request('PUT', 'items/{identifier}/description'.format(identifier=identifier), json={'text': description})
