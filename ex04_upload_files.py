import requests
import sys

from ex02_bearer import bearer_token_for_namespace
from ex03_presign_urls import presign_url
import stacksmith


def upload_file_to_presigned_url(presigned_url, filename):
    with open(filename, 'rb') as f:
        response = requests.put(presigned_url,
            headers={'X-MS-BLOB-TYPE': 'BlockBlob'}, data=f)

    assert response.ok, (
        'Failed to upload "{filename}" to presigned url: {error}'.format(
            filename=filename, error=response.reason))

    return response.ok


def main(args):
    """
    Use the Stacksmith API to generate a pre-signed URL
    and use that URL to upload a file to S3.
    """

    if len(args) < 2:
        print('Must specify a cloud account ID')
        sys.exit(1)

    account_id = args[1]

    namespace = stacksmith.namespace
    bearer_token = bearer_token_for_namespace(namespace)
    filename = 'files/sample.war'

    blob_info = presign_url(namespace, bearer_token, filename, account_id)
    if upload_file_to_presigned_url(blob_info['signedUrl'], filename):
        print('File "{filename}" uploaded to "{blob_uri}"'.format(
            filename=filename,
            blob_uri=blob_info['s3Uri']
        ))


if __name__ == "__main__":
    main(sys.argv)
