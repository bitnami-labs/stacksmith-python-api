from urllib.parse import urljoin
import sys

import requests

from ex02_bearer import bearer_token_for_namespace
import stacksmith


def delete_app(namespace, token, app):
    endpoint = urljoin(
        stacksmith.url,
        'ns/{ns}/apps/{app}'.format(
            ns=namespace,
            app=app
        )
    )
    response = requests.delete(
        endpoint, headers={'authorization': token})

    assert response.status_code == 200, (
        'Failed to delete app "{app}": {error}'.format(
            app=app, error=response.json()['error']))


def main(args):
    """
    Use the Stacksmith API to delete an existing application.
    """

    if len(args) < 2:
        print('Must specify an app ID')
        sys.exit(1)

    app = args[1]
    print('Deleting app "{app}"'.format(app=app))

    namespace = stacksmith.namespace
    bearer_token = bearer_token_for_namespace(namespace)
    delete_app(namespace, bearer_token, app)
    print('Deleted app {app}'.format(app=app))


if __name__ == "__main__":
    main(sys.argv)
