from urllib.parse import urljoin

import requests

from ex02_bearer import bearer_token_for_namespace
import stacksmith


def get_apps(namespace, token):
    endpoint = urljoin(stacksmith.url, 'ns/{ns}/apps'.format(ns=namespace))
    response = requests.get(
        endpoint, headers={'authorization': token})

    assert response.status_code == 200, (
        'Failed to applications for namepsace "{ns}": {error}'.format(
            ns=namespace, error=response.json()['error']))

    return response.json()


def main():
    """
    Use the Stacksmith API to fetch applications for a namespace.
    """
    namespace = stacksmith.namespace

    print('Fetching applications for namespace "{ns}"'.format(ns=namespace))

    bearer_token = bearer_token_for_namespace(namespace)
    apps = get_apps(namespace, bearer_token)

    print('Found {n} applications for namespace "{ns}"'
          .format(n=len(apps), ns=namespace))

    for app in apps:
        print('{name}: {link}'
              .format(name=app['name'], link=app['links']['self']))


if __name__ == "__main__":
    main()
