from quasimodo.auth import AuthConf

import unittest
import os


class AuthConfTest(unittest.TestCase):

    def setUp(self):
        os.environ['QUASIMODO_REDIRECT_URI'] = 'http://example.com'
        os.environ['QUASIMODO_APP_ID'] = '0001112223444555'

    def test_environment_variables_conf(self):
        redirect_url = os.environ.get('QUASIMODO_REDIRECT_URI')
        app_id = os.environ.get('QUASIMODO_APP_ID')

        auth_conf = AuthConf()

        self.assertEqual(auth_conf.redirect_url, redirect_url)
        self.assertEqual(auth_conf.app_id, app_id)


if __name__ == '__main__':
    unittest.main()
