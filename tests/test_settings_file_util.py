import mock
import unittest
import random
from requests import exceptions as request_exception
import sys
from vwo import get_settings_file

if sys.version_info[0] < 3:
    from io import BytesIO as StringIO
else:
    from io import StringIO
account_id = 60781
sdk_key = 'ea87170ad94079aa190bc7c9b85d26fb'


class SettingsFileTest(unittest.TestCase):

    def test_get_settings_file_fires_request(self):
        """ Test that get_settings_file fires off requests call with
        provided account_id and sdk_key. """
        default_random = random.random

        def dummy_random():
            return 0.05353966086631112
        random.random = dummy_random
        with mock.patch('requests.get') as mock_request_get:
            mock_request_get.return_value.status_code = 200
            mock_request_get.return_value.text = 'dummy_setting_file'
            result = get_settings_file(60781, 'ea87170ad94079aa190bc7c9b85d26fb')  # noqa: E501
            self.assertEqual(result, 'dummy_setting_file')

        url = 'https://dev.visualwebsiteoptimizer.com/server-side/settings'
        params = {
            'a': 60781,
            'i': 'ea87170ad94079aa190bc7c9b85d26fb',
            'api-version': 2,
            'r': 0.05353966086631112,
            'platform': 'server',
        }
        mock_request_get.assert_called_once_with(url, params=params)
        random.random = default_random

    def test_get_settings_file_error_status_code(self):
        """ Test that get_settings_file returns None if status_code != 200. """
        default_random = random.random

        def dummy_random():
            return 0.05353966086631112
        random.random = dummy_random
        with mock.patch('requests.get') as mock_request_get, \
                mock.patch('sys.stderr', new=StringIO()) as fakeOutput:
            mock_request_get.return_value.status_code = 503
            mock_request_get.return_value.content = 'Nothing'
            result = get_settings_file(60781, 'ea87170ad94079aa190bc7c9b85d26fb')  # noqa: E501
            self.assertIsNone(result)
            self.assertEqual(fakeOutput.getvalue().strip(),
                             'Request failed for fetching account settings. Got Status Code: 503 and message: Nothing.'  # noqa: E501
                             )
        random.random = default_random

    def test_get_settings_with_exception(self):
        """ Test that get_settings_file raises exception. """
        default_random = random.random

        def dummy_random():
            return 0.05353966086631112
        random.random = dummy_random
        with mock.patch('requests.get',
                        side_effect=request_exception.RequestException('Failed Request')) as mock_request_get, mock.patch('sys.stderr',  # noqa: E501
                                                new=StringIO()
                                                ) as fakeOutput:
            result = get_settings_file(60781,
                                       'ea87170ad94079aa190bc7c9b85d26fb')
            self.assertIsNone(result)
            self.assertEqual(fakeOutput.getvalue().strip(),
                             'Error fetching Settings File Failed Request'
                             )

        url = 'https://dev.visualwebsiteoptimizer.com/server-side/settings'
        params = {
            'a': 60781,
            'i': 'ea87170ad94079aa190bc7c9b85d26fb',
            'api-version': 2,
            'r': 0.05353966086631112,
            'platform': 'server',
        }
        mock_request_get.assert_called_once_with(url, params=params)
        random.random = default_random

    def test_account_id_0_return_none(self):
        result = get_settings_file(0, sdk_key)
        self.assertIsNone(result)

    def test_empty_sdk_key_return_none(self):
        result = get_settings_file(account_id, "")
        self.assertIsNone(result)
