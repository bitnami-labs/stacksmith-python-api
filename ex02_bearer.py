from urllib.parse import urljoin

from pymacaroons import Macaroon
import requests

from ex01_auth import get_auth_macaroon
import stacksmith


DISCHARGE_ENDPOINT = urljoin(stacksmith.url, 'authn/discharge')


def get_service_macaroon(namespace):
    endpoint = urljoin(stacksmith.url, 'ns/{ns}/apps'.format(ns=namespace))
    response = requests.get(endpoint, headers={'service-macaroon': 'request'})
    assert 'service-macaroon' in response.headers, 'Service macaroon missing.'
    return Macaroon.deserialize(response.headers['service-macaroon'])


def get_discharge(auth_macaroon, service_macaroon):
    caveat_ids = [c.caveat_id for c in service_macaroon.third_party_caveats()]
    data = {
        'discharges': caveat_ids,
        'authMacaroon': auth_macaroon.serialize(),
    }
    discharge_response = requests.post(DISCHARGE_ENDPOINT, json=data)
    assert discharge_response.status_code == 200, 'Discharge failed.'
    return discharge_response.json()


def make_bearer(service_macaroon, discharge):
    discharge_macaroons = [
        Macaroon.deserialize(m) for m in discharge['dischargeMacaroons']]
    return 'Bearer {0} {1}'.format(
        service_macaroon.serialize(),
        ' '.join(service_macaroon.prepare_for_request(m).serialize()
                 for m in discharge_macaroons))


def bearer_token_for_namespace(namespace):
    service_macaroon = get_service_macaroon(namespace)

    if not stacksmith.auth_macaroon:
        auth_macaroon = get_auth_macaroon()
    else:
        auth_macaroon = Macaroon.deserialize(stacksmith.auth_macaroon)

    discharge = get_discharge(auth_macaroon, service_macaroon)
    bearer = make_bearer(service_macaroon, discharge)
    return bearer


def main():
    """
    Use an Authorization Macaroon to obtain a Bearer token for a
    given namespace which can be used to make further API calls to
    that namespace.
    """
    bearer = bearer_token_for_namespace(stacksmith.namespace)
    print(bearer)


if __name__ == "__main__":
    main()
