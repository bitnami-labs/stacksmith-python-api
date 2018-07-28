from urllib.parse import urljoin
import sys

import requests

from ex02_bearer import bearer_token_for_namespace
import stacksmith


def get_update_preview_for_build(namespace, token, build):
    packages_preview_endpoint = urljoin(
        stacksmith.url,
        'ns/{ns}/builds/{build}/system-packages/preview'.format(
            ns=namespace,
            build=build
        )
    )
    response = requests.get(
        packages_preview_endpoint, headers={'authorization': token})

    assert response.status_code == 200, (
        'Could not get packages preview for build "{build}": {reason}'.format(
            build=build, error=response.json()['error']))

    return response.json()


def main(args):
    """
    Use the Stacksmith API to retrieve the system packages that will be
    updated by performing a rebuild.
    """
    namespace = stacksmith.namespace
    bearer_token = bearer_token_for_namespace(namespace)

    if len(args) < 2:
        print('Must specify a build ID')
        sys.exit(1)

    build = args[1]
    preview = get_update_preview_for_build(namespace, bearer_token, build)
    print(preview)
    print('{num_pkgs} packages will be updated by rebuilding build "{build}"'
          .format(num_pkgs=len(preview), build=build))


if __name__ == "__main__":
    main(sys.argv)
