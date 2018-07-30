from urllib.parse import urljoin
import os

import requests

from ex02_bearer import bearer_token_for_namespace
from ex03_presign_urls import presign_url
from ex04_upload_files import upload_file_to_presigned_url
import stacksmith


def upload_application_files(namespace, token, files):
    app_files = []
    for f in files:
        blob_info = presign_url(namespace, token, f)

        if upload_file_to_presigned_url(blob_info['signedUrl'], f):
            app_files.append({
                'filename': os.path.basename(f),
                'blobPath': blob_info['blobUri']
            })
        else:
            print('Warning: Failed to upload file "{}"'.format(f))

    return app_files


def upload_application_scripts(namespace, token, scripts):
    app_scripts = {}
    for script_type, script_file in scripts.items():
        blob_info = presign_url(namespace, token, script_file)

        if upload_file_to_presigned_url(blob_info['signedUrl'], script_file):
            app_scripts[script_type] = {
                'blobPath': blob_info['blobUri']
            }

    return app_scripts


def create_application(
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


def main():
    """
    Use the Stacksmith API to create an application.
    Within this sample, a Bearer token will be generated,
    the necessary files will be uploaded to S3,
    and the build will be started.
    """
    namespace = stacksmith.namespace
    bearer_token = bearer_token_for_namespace(namespace)
    files = ['files/sample.war']
    app_files = upload_application_files(namespace, bearer_token, files)

    scripts = {
        'build': 'files/build.sh',
        'entrypoint': 'files/entrypoint.sh'
    }
    app_scripts = upload_application_scripts(namespace, bearer_token, scripts)

    new_app = create_application(
        namespace, bearer_token,
        'test-app', '1.0', 'tomcat', ['docker'], app_files, app_scripts)

    print(new_app)


if __name__ == "__main__":
    main()
