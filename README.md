# Stacksmith API Samples

This directory contains a number of sample files which show how you can interact with the
Stacksmith API.

## Running the samples
All examples require the `STACKSMITH_NAMESPACE` environment variable set, this can point to any
namespace you have access to, in general you want to set this to your account email.

Also examples listed here require a [Bitnami](https://bitnami.com) login that can be created as
part of the authorization flow. Each sample will trigger the full authorization flow unless the
`STACKSMITH_AUTH_MACAROON` environment variable is provided which can be obtained by the execution
of `ex01_auth.py`. These code samples are written in Python 3 and can be run using the provided
Dockerfile:

```
docker build -t stacksmith-samples .

docker run -v $PWD:/app \
  -p 8551:8551 \
  -e STACKSMITH_NAMESPACE=$STACKSMITH_NAMESPACE \
  -e STACKSMITH_AUTH_MACAROON=$STACKSMITH_AUTH_MACAROON \
  -it stacksmith-samples python <filename.py>
```

There's a shortcut `run.sh` script provided that takes care of all details for you and in the case
of obtaining the Auth Macaroon will also take care of spawning the browser to the login URL:

```
export STACKSMITH_NAMESPACE=user@example.com
./run.sh ex01_auth.py
```

If you want to avoid having to manually log in again next time, just execute this in your shell:

```
export STACKSMITH_AUTH_MACAROON="<Auth Macaroon output>"
```

## Sample types
There are 16 code samples available:

* ex01_auth.py: Authenticating with Stacksmith and obtaining an Authorization Macaroon.
* ex02_bearer.py: Using an Authorization Macaroon to obtain a Bearer token for a given namespace
which can be used to make further API calls to that namespace.
* ex03_presign_urls.py: Using the Stacksmith API to generate a pre-signed URL which can be used to
upload a file to S3.
* ex04_upload_files.py: Using a generated pre-signed URL to upload a file to S3.
* ex05_create_app.py: Using the Stacksmith API to create an application. Within this sample, a
Bearer token will be generated, the necessary files will be uploaded to S3, and the build will be
started.
* ex06_build_details.py: Retrieving the details of an existing build.
* ex07_build_logs.py: Retrieving and printing the logs for a build.
* ex08_waiting_for_build.py: Waiting for a build to complete.
* ex09_existing_apps.py: Retrieving existing applications for a namespace.
* ex10_app_details.py: Retrieving the details of an existing application.
* ex11_edit_app.py: Editing and submitting a new revision of an application.
* ex12_rebuild.py: Triggering a rebuild of an application.
* ex13_delete_app.py: Deleting an application.
* ex14_download_artifacts.py: Downloading the artifacts from a build.
* ex15_system_packages.py: Retrieving the list of system packages installed as part of a build.
* ex16_system_packages_preview.py: Retrieving the preview list of system packages which will be
installed as part of rebuilding an build.
