import mock
import unittest
from vwo.http import connection


class ConnectionTest(unittest.TestCase):

    def setUp(self):
        self.connection = connection.Connection()

    def test_connection_get_with_exception(self):
        with mock.patch('requests.Session.get',
                        side_effect=Exception('REQUEST FAILED')):
            result = self.connection.get('https://vwo.com/')
            self.assertDictEqual(result, {'status_code': None, 'text': ''})
