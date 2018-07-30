from urllib.parse import urljoin
import os
import sys

import requests

from ex02_bearer import bearer_token_for_namespace
from ex03_presign_urls import presign_url
from ex04_upload_files import upload_file_to_presigned_url
import stacksmith


def upload_application_files(namespace, token, files, account_id):
    app_files = []
    for f in files:
        blob_info = presign_url(namespace, token, f, account_id)

        if upload_file_to_presigned_url(blob_info['signedUrl'], f):
            app_files.append({
                'filename': os.path.basename(f),
                'storageURI': blob_info['s3Uri']
            })
        else:
            print('Warning: Failed to upload file "{}"'.format(f))

    return app_files


def upload_application_scripts(namespace, token, scripts, account_id):
    app_scripts = {}
    for script_type, script_file in scripts.items():
        blob_info = presign_url(namespace, token, script_file, account_id)

        if upload_file_to_presigned_url(blob_info['signedUrl'], script_file):
            app_scripts[script_type] = {
                'storageURI': blob_info['s3Uri']
            }

    return app_scripts


def create_application(
    cloudAccountID,
    namespace,
    token,
    app_name,
    app_version,
    template,
    targets,
    app_files,
    app_scripts
):
    app_data = {
        'cloudAccountID': cloudAccountID,
        'appName': app_name,
        'appVersion': app_version,
        'template': template,
        'targets': targets,
        'appFiles': app_files,
        'appScripts': app_scripts
    }
    new_app_endpoint = urljoin(
        stacksmith.url, 'ns/{namespace}/apps'.format(namespace=namespace))
    response = requests.post(
        new_app_endpoint, headers={'Authorization': token}, json=app_data)

    assert response.status_code == 201, (
        'Failed to create new application "{app_name}": {error}'.format(
            app_name=app_name, error=response.json()['error']))

    return response.json()


def main(args):
    """
    Use the Stacksmith API to create an application.
    Within this sample, a Bearer token will be generated,
    the necessary files will be uploaded to S3,
    and the build will be started.
    """


    if len(args) < 2:
        print('Must specify a cloud account ID. Use ex16_get_cloud_accounts.py to retrieve it.')
        sys.exit(1)

    account_id = args[1]

    namespace = stacksmith.namespace
    bearer_token = bearer_token_for_namespace(namespace)
    files = ['files/sample.war']
    app_files = upload_application_files(namespace, bearer_token, files, account_id)


    scripts = {
        'build': 'files/build.sh',
        'entrypoint': 'files/entrypoint.sh'
    }
    app_scripts = upload_application_scripts(namespace, bearer_token, scripts, account_id)

    new_app = create_application(
        account_id,
        namespace,
        bearer_token,
        'test-app',
        '1.0',
        'TOMCAT',
        ['azure'],
        app_files,
        app_scripts)

    print(new_app)


if __name__ == "__main__":
    main(sys.argv)
