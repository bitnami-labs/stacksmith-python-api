from urllib.parse import urljoin
import shutil
import sys

import requests

from ex02_bearer import bearer_token_for_namespace
import stacksmith


def get_downloadable_artifacts(namespace, token, build):
    download_endpoint = urljoin(
        stacksmith.url,
        'ns/{ns}/builds/{build}/downloadUrl/{artifact}'.format(
            ns=namespace,
            build=build,
            artifact='template_s3_uri'
        )
    )
    download = requests.get(
        download_endpoint, headers={'authorization': token})

    assert download.status_code == 200, (
        'Could not get artifacts for build "{build}": {reason}'.format(
            build=build, reason=download.json().get('error')))

    return download.json().get('filename'), download.json().get('url')


def download_artifacts(namespace, token, build):
    filename, url = get_downloadable_artifacts(namespace, token, build)

    download = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        download.raw.decode_content = True
        shutil.copyfileobj(download.raw, f)

    return filename


def main(args):
    """
    Use the Stacksmith API to download artifacts for a build.
    """

    if len(args) < 2:
        print('Must specify a build ID')
        sys.exit(1)

    build = args[1]
    namespace = stacksmith.namespace
    bearer_token = bearer_token_for_namespace(namespace)
    filename = download_artifacts(namespace, bearer_token, build)
    print('Downloaded artifacts from "{build}" to "{filename}"'.format(
        build=build,
        filename=filename
    ))


if __name__ == "__main__":
    main(sys.argv)
