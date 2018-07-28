from urllib.parse import urljoin
import os
import requests
import sys

from ex02_bearer import bearer_token_for_namespace
import stacksmith


def presign_url(namespace, bearer_token, filename, account_id):
    endpoint = urljoin(
        stacksmith.url, 'ns/{namespace}/s3sign'.format(namespace=namespace))
    data = {'objectName': os.path.basename(filename), 'cloudAccountID': account_id}
    response = requests.post(
        endpoint, headers={'Authorization': bearer_token}, json=data)

    assert response.status_code == 201, (
        'Failed to create pre-signed URL for "{filename}": {error}'.format(
            filename=filename, error=response.json()['error']))

    return response.json()


def main(args):
    """
    Use the Stacksmith API to generate a pre-signed URL which
    can be used to upload a file to S3.
    """

    if len(args) < 2:
        print('Must specify a cloud account ID')
        sys.exit(1)

    account_id = args[1]

    namespace = stacksmith.namespace
    bearer_token = bearer_token_for_namespace(namespace)
    print(presign_url(namespace, bearer_token, 'sample.war', account_id))

if __name__ == "__main__":
    main(sys.argv)
