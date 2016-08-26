import unittest
from urllib.parse import urlencode

from quasimodo.auth import AuthConf, AuthURL


APP_ID = '91624454549617'
SECRET_KEY = 'iaw2fxRXjRM5mj4qpJkMX'

auth_conf = AuthConf(APP_ID, SECRET_KEY)

class AuthConfTest(unittest.TestCase):
    def test_properties(self):
        assert auth_conf.app_id == APP_ID
        assert auth_conf.secret_key == SECRET_KEY


class AuthURLTest(unittest.TestCase):
    def test_return(self):
        auth_url = AuthURL(auth_conf)
        params = {
            'response_type': 'code',
            'client_id': APP_ID
        }

        assert repr(auth_url) == 'http://auth.mercadolibre.com/authorization?{}'.format(urlencode(params))

    def test_parameters(self):
        response_type = 'hex'
        redirect_uri = 'http://example.com'

        auth_url = AuthURL(auth_conf, redirect_uri='http://example.com', response_type='hex')
        params = {
            'response_type': response_type,
            'redirect_uri': redirect_uri,
            'client_id': APP_ID
        }

        assert repr(auth_url) == 'http://auth.mercadolibre.com/authorization?{}'.format(urlencode(params))
