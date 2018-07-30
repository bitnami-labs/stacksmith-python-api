from urllib.parse import urljoin
import sys

import requests

from ex02_bearer import bearer_token_for_namespace
from ex10_app_details import get_app_details
import stacksmith


def edit_application(
    namespace,
    cloudAccountID,
    token,
    app_id,
    app_version,
    template,
    targets,
    app_files,
    app_scripts
):
    app_data = {
        'cloudAccountID': cloudAccountID,
        'appVersion': app_version,
        'template': template,
        'targets': targets,
        'appFiles': app_files,
        'appScripts': app_scripts
    }

    edit_app_endpoint = urljoin(
        stacksmith.url,
        'ns/{namespace}/apps/{app_id}/revisions'.format(
            namespace=namespace, app_id=app_id)
    )
    response = requests.post(
        edit_app_endpoint, headers={'Authorization': token}, json=app_data)

    assert response.status_code == 201, (
        'Failed to edit app "{app}": {error}'.format(
            app=app_id, error=response.json()['error']))

    return response.json()


def get_latest_revision(namespace, token, app_id):
    app_details = get_app_details(namespace, token, app_id)

    response = requests.get(
        app_details['latestRevision']['links']['self'],
        headers={'Authorization': token}
    )

    assert response.status_code == 200, (
        'Failed to get latest revision for app "{app}": {error}'.format(
            app=app_id, error=response.json()['error']))

    return response.json()


def main(args):
    """
    Use the Stacksmith API to edit an application.
    Within this sample, the latest revision of the provided application
    will be fetched, and a new revision will be submitted with a new version.
    """

    if len(args) < 3:
        print('Must specify an application ID and cloud account ID')
        sys.exit(1)

    app_id = args[1]
    cloudAccountID = args[2]
    print('Editing application "{app}"'.format(app=app_id))

    namespace = stacksmith.namespace
    bearer_token = bearer_token_for_namespace(namespace)
    latest_revision = get_latest_revision(namespace, bearer_token, app_id)
    edited_app = edit_application(
        namespace,
        cloudAccountID,
        bearer_token,
        app_id,
        '2.0',
        latest_revision['template'],
        [t['name'] for t in latest_revision['targets']],
        latest_revision['appFiles'],
        latest_revision.get('appScripts'))
    print(edited_app)


if __name__ == "__main__":
    main(sys.argv)
