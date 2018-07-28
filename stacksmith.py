"""
Things related to Stacksmith
"""
import os


url = (
    os.getenv('STACKSMITH_API_URL') or
    'https://beta.stacksmith.bitnami.com/api/v1/')
namespace = os.getenv('STACKSMITH_NAMESPACE')
auth_macaroon = os.getenv('STACKSMITH_AUTH_MACAROON')


assert namespace, (
    'Must specify a namespace using the STACKSMITH_NAMESPACE '
    'environment variable.')
