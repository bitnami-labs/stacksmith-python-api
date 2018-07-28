from urllib.parse import urljoin
import sys

import requests

from ex02_bearer import bearer_token_for_namespace
import stacksmith


def get_build_details(namespace, token, build):
    endpoint = urljoin(
        stacksmith.url,
        'ns/{ns}/builds/{build}'.format(
            ns=namespace,
            build=build
        )
    )
    response = requests.get(
        endpoint, headers={'authorization': token})

    assert response.status_code == 200, (
        'Failed to fetch details for build "{build}": {error}'.format(
            build=build, error=response.json()['error']))

    return response.json()


def main(args):
    """
    Use the Stacksmith API to fetch details of a build.
    """

    if len(args) < 2:
        print('Must specify a build ID')
        sys.exit(1)

    build = args[1]
    print('Fetching details for build "{build}"'.format(build=build))

    namespace = stacksmith.namespace
    bearer_token = bearer_token_for_namespace(namespace)
    build_details = get_build_details(namespace, bearer_token, build)
    print(build_details)


if __name__ == "__main__":
    main(sys.argv)
