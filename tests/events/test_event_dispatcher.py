import mock
import unittest

from vwo.event import event_dispatcher
from vwo.services import singleton


class DispatcherTest(unittest.TestCase):

    def setUp(self):
        self.dispatcher = event_dispatcher.EventDispatcher()

    def tearDown(self):
        singleton.forgetAllSingletons()

    def test_dispatch_fires_request(self):
        """ Test that dispatch event fires off requests call with provided URL
        and params. """

        properties = {
            'uId': 'shravan',
            'combination': 1,
            'url': 'https://dev.visualwebsiteoptimizer.com/server-side/track-user',
            'ed': '{"p": "server"}',
            'random': 0.7382938446947298,
            'ap': 'server',
            'u': '09CD6107E42B51F9BFC3DD97EA900990',
            'experiment_id': 229,
            'sId': 1565949670,
            'sdk-v': '1.0.2',
            'sdk': 'python',
            'account_id': 60781,
        }

        with mock.patch('vwo.http.connection.Connection.get') as mock_request_get:
            mock_request_get.return_value = {'status_code': 200, 'text': ''}
            result = self.dispatcher.dispatch(properties)
            self.assertIs(result, True)

        url = properties.get('url')
        del properties['url']
        mock_request_get.assert_called_once_with(url, params=properties)

    def test_dispatch_error_status_code(self):
        """ Test that dispatch returns False if status_code != 200. """
        properties = {
            'uId': 'shravan',
            'combination': 1,
            'url': 'https://dev.visualwebsiteoptimizer.com/server-side/track-user',
            'ed': '{"p": "server"}',
            'random': 0.7382938446947298,
            'ap': 'server',
            'u': '09CD6107E42B51F9BFC3DD97EA900990',
            'experiment_id': 229,
            'sId': 1565949670,
            'sdk-v': '1.0.2',
            'sdk': 'python',
            'account_id': 60781,
        }

        with mock.patch('vwo.http.connection.Connection.get') as mock_request_get:
            mock_request_get.return_value.status_code = 503
            result = self.dispatcher.dispatch(properties)
            self.assertIs(result, False)
