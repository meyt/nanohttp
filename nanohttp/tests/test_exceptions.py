
import unittest

import ujson

from nanohttp import Controller, html, HttpBadRequest, json, HttpStatus, \
    settings
from nanohttp.tests.helpers import WsgiAppTestCase


class ExceptionTestCase(WsgiAppTestCase):

    class Root(Controller):
        @html
        def index(self):
            raise HttpBadRequest()

        @json
        def data(self):
            raise HttpBadRequest()

        @json
        def custom(self):
            raise HttpStatus(status='462 custom text')

        @html
        def err(self):
            x = 1 / 0
            return 'test'

    def test_exception(self):
        response, content = self.assert_get('/', status=400)
        self.assertIsNotNone(content)

        response, content = self.assert_get('/data', status=400)
        self.assertIn('stackTrace', ujson.loads(content))
        self.assertIsNotNone('stackTrace', ujson.loads(content))

        response, content = self.assert_get('/err', status=500)
        self.assertIsNotNone(content)

        settings.debug = False

        response, content = self.assert_get('/', status=400)
        self.assertEqual(content, b'')

        response, content = self.assert_get('/data', status=400)
        self.assertNotIn('stackTrace', ujson.loads(content))

    def test_custom_exception(self):
        response, content = self.assert_get('/custom', status=462)

        self.assertIn('stackTrace', ujson.loads(content))
        self.assertIsNotNone('stackTrace', ujson.loads(content))


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
