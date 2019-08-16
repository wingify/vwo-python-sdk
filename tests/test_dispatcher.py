import mock
import unittest

from vwo import event_dispatcher
from vwo.helpers import singleton


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
            'url': 'https://dev.visualwebsiteoptimizer.com/server-side/track-user',  # noqa: E501
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

        with mock.patch('requests.get') as mock_request_get:
            mock_request_get.return_value.status_code = 200
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
            'url': 'https://dev.visualwebsiteoptimizer.com/server-side/track-user',  # noqa: E501
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

        with mock.patch('requests.get') as mock_request_get:
            mock_request_get.return_value.status_code = 503
            result = self.dispatcher.dispatch(properties)
            self.assertIs(result, False)

    def test_dispatch_with_exception(self):
        """ Test that dispatch returns False if exception occurs. """
        properties = {
            'uId': 'shravan',
            'combination': 1,
            'url': 'https://dev.visualwebsiteoptimizer.com/server-side/track-user',  # noqa: E501
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

        with mock.patch('requests.get',
                        side_effect=Exception('IMPRESSION FAILED')):
            result = self.dispatcher.dispatch(properties)
            self.assertIs(result, False)
