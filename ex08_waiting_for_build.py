import sys
import time

from ex02_bearer import bearer_token_for_namespace
from ex06_build_details import get_build_details
import stacksmith


def get_build_status(namespace, token, build):
    return get_build_details(namespace, token, build)['status']


def wait_for_build(namespace, token, build):
    status = get_build_status(namespace, token, build)

    while status not in ['finished', 'failed', 'aborted']:
        print('Build "{build}" not completed ({status}). '
              'Waiting 10 seconds...'.format(build=build, status=status))
        time.sleep(10)
        status = get_build_status(namespace, token, build)

    return status


def main(args):
    """
    Use the Stacksmith API to wait for a build to complete.
    """

    if len(args) < 2:
        print('Must specify a build ID')
        sys.exit(1)

    build = args[1]
    print('Fetching details for build "{build}"'.format(build=build))

    namespace = stacksmith.namespace
    bearer_token = bearer_token_for_namespace(namespace)
    status = wait_for_build(namespace, bearer_token, build)
    print('Build "{build}" completed with status "{status}"'.format(
        build=build, status=status))


if __name__ == "__main__":
    main(sys.argv)
