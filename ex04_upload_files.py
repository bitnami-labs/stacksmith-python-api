import requests

from ex02_bearer import bearer_token_for_namespace
from ex03_presign_urls import presign_url
import stacksmith


def upload_file_to_presigned_url(presigned_url, filename):
    with open(filename, 'rb') as f:
        response = requests.put(presigned_url, data=f)

    assert response.ok, (
        'Failed to upload "{filename}" to presigned url: {error}'.format(
            filename=filename, error=response.reason))

    return response.ok


def main():
    """
    Use the Stacksmith API to generate a pre-signed URL
    and use that URL to upload a file to S3.
    """
    namespace = stacksmith.namespace
    bearer_token = bearer_token_for_namespace(namespace)
    filename = 'files/sample.war'

    blob_info = presign_url(namespace, bearer_token, filename)
    if upload_file_to_presigned_url(blob_info['signedUrl'], filename):
        print('File "{filename}" uploaded to "{blob_uri}"'.format(
            filename=filename,
            blob_uri=blob_info['blobUri']
        ))


if __name__ == "__main__":
    main()
