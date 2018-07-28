from urllib.parse import urljoin
import sys

import requests

from ex02_bearer import bearer_token_for_namespace
import stacksmith


def start_rebuild(namespace, token, build):
    endpoint = urljoin(
        stacksmith.url,
        'ns/{ns}/builds/{build}/rebuild'.format(
            ns=namespace,
            build=build
        )
    )
    response = requests.post(
        endpoint, headers={'authorization': token})

    assert response.status_code == 201, (
        'Failed to start rebuild of build "{build}": {error}'.format(
            build=build, error=response.json()['error']))

    return response.json()


def main(args):
    """
    Use the Stacksmith API to perform a rebuild of an application build.
    """

    if len(args) < 2:
        print('Must specify a build ID')
        sys.exit(1)

    build = args[1]
    print('Starting rebuild of build "{build}"'.format(build=build))

    namespace = stacksmith.namespace
    bearer_token = bearer_token_for_namespace(namespace)
    rebuild = start_rebuild(namespace, bearer_token, build)
    print(rebuild)


if __name__ == "__main__":
    main(sys.argv)
