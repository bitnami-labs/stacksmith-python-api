from urllib.parse import urljoin
import os

import requests

from ex02_bearer import bearer_token_for_namespace
import stacksmith


def presign_url(namespace, bearer_token, filename):
    endpoint = urljoin(
        stacksmith.url, 'ns/{namespace}/s3sign'.format(namespace=namespace))
    data = {'objectName': os.path.basename(filename)}
    response = requests.post(
        endpoint, headers={'Authorization': bearer_token}, json=data)

    assert response.status_code == 201, (
        'Failed to create pre-signed URL for "{filename}": {error}'.format(
            filename=filename, error=response.json()['error']))

    return response.json()


def main():
    """
    Use the Stacksmith API to generate a pre-signed URL which
    can be used to upload a file to S3.
    """
    namespace = stacksmith.namespace
    bearer_token = bearer_token_for_namespace(namespace)
    print(presign_url(namespace, bearer_token, 'sample.war'))


if __name__ == "__main__":
    main()
