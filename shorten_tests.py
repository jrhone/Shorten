import os
import shorten
import unittest
import tempfile

import simplejson as json

class ShortenTestCase(unittest.TestCase):

    def setUp(self):
        self.app = shorten.app.test_client()

    def tearDown(self):
        self.app = None

    def add_url(self, long_url, custom_code=None):
        data = {}
        if custom_code is not None:
            data['custom_short_code'] = custom_code
        data['long_url'] = long_url

        return self.app.post('/shorten_url', data=json.dumps(data))

    def verify_redirect(self, short_code):
        return self.app.get('/%s' % short_code, follow_redirects=True)

    def test_shorten_success(self):
        rv = self.add_url("www.google.com", "a")

        response = json.loads(rv.data)
        assert 'success' in rv.response
        assert 'short_code' in rv.response       
        assert 'True' is rv.response['success']

        rv = self.add_url("http://www.google.com", "b")

        response = json.loads(rv.data)
        assert 'success' in rv.response
        assert 'short_code' in rv.response       
        assert 'True' is rv.response['success']

    def test_shorten_failure(self):
        rv = self.add_url("www.google.com", "a")
        rv = self.add_url("www.google.com", "a")

        response = json.loads(rv.data)
        assert 'success' in rv.response
        assert 'False' is rv.response['success']  


    def test_shorten_no_custom(self):
        rv = self.add_url("www.google.com")
        rv = self.add_url("www.google.com")
        rv = self.add_url("www.google.com")

        response = json.loads(rv.data)
        assert 'success' in rv.response
        assert 'short_code' in rv.response       
        assert 'True' is rv.response['success']

    def test_redirect_success(self):
        rv = self.add_url("www.google.com", "a")
        response = json.loads(rv.data)
        short_code = rv.response[response['short_code']]

        self.verify_redirect(short_code)
        assert True


    def test_redirect_failure(self):
        self.verify_redirect("short_code")
        assert True


if __name__ == '__main__':
    unittest.main()
