from urllib.parse import urljoin
import os

import requests

from ex02_bearer import bearer_token_for_namespace
import stacksmith


def get_cloud_accounts(namespace, bearer_token):
    endpoint = urljoin(
        stacksmith.url, 'ns/{namespace}/cloud-accounts'.format(namespace=namespace))
    response = requests.get(
        endpoint, headers={'Authorization': bearer_token})

    assert response.status_code == 200, (
        'Failed to get cloud accounts for "{namespace}": {error}'.format(
            namespace=namespace, error=response.json()['error']))

    return response.json()


def main():
    """
    Use the Stacksmith API to get a list of all cloud accounts.
    """
    namespace = stacksmith.namespace
    bearer_token = bearer_token_for_namespace(namespace)
    print(get_cloud_accounts(namespace, bearer_token))


if __name__ == "__main__":
    main()
