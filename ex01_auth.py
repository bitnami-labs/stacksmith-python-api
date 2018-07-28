from urllib.parse import parse_qs, urlencode, urljoin
from wsgiref.simple_server import (
    WSGIRequestHandler as BaseWSGIRequestHandler,
    make_server,
)
from wsgiref.util import setup_testing_defaults
import sys

from pymacaroons import Macaroon

import stacksmith


AUTHORIZE_ENDPOINT = urljoin(stacksmith.url, 'authn/oauth2/authorize')
REDIRECT_PORT = 8551
REDIRECT_URI = 'http://localhost:{port}'.format(port=REDIRECT_PORT)
TEMPLATE = """
<html>
  <head>
    <title>Stacksmith auth</title>
  </head>
  <body>
    <p>{message}</p>
    <script>setTimeout(window.close, 5000);</script>
  </body>
</html>
"""


class AuthMacaroonHandler():
    def __init__(self):
        self.auth_macaroon = None

    def extract_auth_macaroon(self, environ, start_response):
        setup_testing_defaults(environ)

        status = '200 OK'
        headers = [('Content-type', 'text/html; charset=utf-8')]

        start_response(status, headers)

        query_string = parse_qs(environ.get('QUERY_STRING'))
        if not query_string:
            msg = 'No query string found, retry. Closing window...'
        elif 'authMacaroon' not in query_string:
            msg = 'No authMacaroon in query string, retry. Closing window...'
        else:
            msg = (
                'Authenticated. Please switch back to your shell.'
                ' Closing window...')
            self.auth_macaroon = Macaroon.deserialize(
                query_string['authMacaroon'][0])

        return [TEMPLATE.format(message=msg).encode()]


def get_auth_macaroon():
    if stacksmith.auth_macaroon:
        return Macaroon.deserialize(stacksmith.auth_macaroon)

    # Strip default request logs from server.
    class WSGIRequestHandler(BaseWSGIRequestHandler):
        def log_request(self, code='-', size='-'):
            pass

    handler = AuthMacaroonHandler()
    httpd = make_server(
        '', REDIRECT_PORT, handler.extract_auth_macaroon,
        handler_class=WSGIRequestHandler)
    httpd.handle_request()

    assert handler.auth_macaroon is not None, 'No Auth Macaroon found, retry.'
    return handler.auth_macaroon


def main():
    """
    Authenticate with Stacksmith and obtain an Authorization Macaroon.
    """
    url = "{endpoint}?{args}".format(
        endpoint=AUTHORIZE_ENDPOINT,
        args=urlencode({'redirect_uri': REDIRECT_URI}))
    print("Please open this URL in your browser: {url}\n"
          .format(url=url), file=sys.stderr)

    auth_macaroon = get_auth_macaroon()
    print('Successfully authenticated. Execute the following in your shell '
          'to add the authentication macaroon to your environment for further '
          'samples: \n', file=sys.stderr)
    print('export STACKSMITH_AUTH_MACAROON="{macaroon}"'.format(
        macaroon=auth_macaroon.serialize()))


if __name__ == "__main__":
    main()
