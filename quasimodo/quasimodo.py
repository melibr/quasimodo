from auth import AuthConf, AuthURL, AuthorizationCode


class Quasimodo:
    def __init__(self, app_id, secret_key):
        self._auth_conf = AuthConf(app_id, secret_key)

    def auth_url(self, redirect_uri=None):
        return AuthURL(self._auth_conf, redirect_uri)

    def authorize(self, code, redirect_uri):
        authorization_code = AuthorizationCode(self._auth_conf, code, redirect_uri)
        self._credentials = authorization_code.credentials
        return self._credentials

    @property
    def access_token(self):
        return self._credentials.get('access_token')

    @property
    def expires_in(self):
        expires = int(self._credentials.get('expires_in', 0))

        if expires > 0:
            return {
                'seconds': expires,
                'minutes': expires / 60,
                'hours': (expires / 60) / 60,
            }

    @property
    def user_id(self):
        return self._credentials.get('user_id')

    @property
    def refresh_token(self):
        return self._credentials.get('refresh_token')
