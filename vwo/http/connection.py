""" Module for making requests, uses requests internally """

import requests


class Connection:
    def __init__(self):
        self.session = requests.Session()

    def get(self, url, params=None):
        try:
            resp = self.session.get(url, params=params)
            return {
                'status_code': resp.status_code,
                'text': resp.text
            }
        except Exception:
            return {
                'status_code': None,
                'text': ''
            }

    def post(self, url, params=None, data=None):
        try:
            resp = self.session.post(url, params=params, json=data)
            return {
                'status_code': resp.status_code,
                'text': resp.text
            }
        except Exception:
            return {
                'status_code': None,
                'text': ''
            }
