from urllib.parse import urljoin
import sys

import requests

from ex02_bearer import bearer_token_for_namespace
import stacksmith


def get_system_packages_for_build(namespace, token, build):
    system_pkgs_endpoint = urljoin(
        stacksmith.url,
        'ns/{ns}/builds/{build}/system-packages'.format(
            ns=namespace,
            build=build
        )
    )
    response = requests.get(
        system_pkgs_endpoint, headers={'authorization': token})

    assert response.status_code == 200, (
        'Could not get system packages for build "{build}": {reason}'.format(
            build=build, error=response.json()['error']))

    return response.json()


def main(args):
    """
    Use the Stacksmith API to retrieve the system packages that were
    installed as part of a build.
    """
    namespace = stacksmith.namespace
    bearer_token = bearer_token_for_namespace(namespace)

    if len(args) < 2:
        print('Must specify a build ID')
        sys.exit(1)

    build = args[1]
    packages = get_system_packages_for_build(namespace, bearer_token, build)
    print('{num_pkgs} packages were installed as part of build "{build}"'
          .format(num_pkgs=len(packages), build=build))
    print(packages[:10])


if __name__ == "__main__":
    main(sys.argv)
