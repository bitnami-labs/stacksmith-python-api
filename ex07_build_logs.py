from urllib.parse import urljoin
import sys
import time

import requests

from ex02_bearer import bearer_token_for_namespace
from ex06_build_details import get_build_details
import stacksmith


def get_build_logs_url(build):
    jobs = [job for job in build['stackbuilderInfo']['jobs']
            if job['type'] == 'imagebuilder']
    job_name = jobs[0]['name']
    return urljoin(stacksmith.url,
                   'logreader/getlogs/{job_name}'.format(job_name=job_name))


def get_build_logs(namespace, token, build):
    build_details = get_build_details(namespace, token, build)
    logs_url = get_build_logs_url(build_details)

    while True:
        log_response = requests.get(logs_url, stream=True)
        if log_response.status_code == 200:
            break
        print('Logs for build "{build}" are not yet available. '
              'Waiting 10 seconds...'.format(build=build))
        time.sleep(10)

    for line in log_response.iter_lines():
        if line:
            print(line.decode())


def main(args):
    """
    Use the Stacksmith API to fetch and print the logs for a build.
    """

    if len(args) < 2:
        print('Must specify a build ID')
        sys.exit(1)

    build = args[1]
    print('Fetching logs for build "{build}"'.format(build=build))

    namespace = stacksmith.namespace
    bearer_token = bearer_token_for_namespace(namespace)

    get_build_logs(namespace, bearer_token, build)


if __name__ == "__main__":
    main(sys.argv)
