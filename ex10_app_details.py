from urllib.parse import urljoin
import sys

import requests

from ex02_bearer import bearer_token_for_namespace
import stacksmith


def get_app_details(namespace, token, app):
    endpoint = urljoin(
        stacksmith.url,
        'ns/{ns}/apps/{app}'.format(
            ns=namespace,
            app=app
        )
    )
    response = requests.get(
        endpoint, headers={'authorization': token})

    assert response.status_code == 200, (
        'Failed to fetch details for app "{app}": {error}'.format(
            app=app, error=response.json()['error']))

    return response.json()


def main(args):
    """
    Use the Stacksmith API to fetch details of an application.
    """

    if len(args) < 2:
        print('Must specify an app ID')
        sys.exit(1)

    app = args[1]
    print('Fetching details for app "{app}"'.format(app=app))

    namespace = stacksmith.namespace
    bearer_token = bearer_token_for_namespace(namespace)
    app_details = get_app_details(namespace, bearer_token, app)
    print(app_details)


if __name__ == "__main__":
    main(sys.argv)
