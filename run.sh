#!/usr/bin/env bash

set -euo pipefail

readonly STACKSMITH_API_URL=${STACKSMITH_API_URL:-'https://stacksmith.bitnami.com/api/v1/'}
readonly STACKSMITH_AUTH_MACAROON=${STACKSMITH_AUTH_MACAROON:-''}
readonly STACKSMITH_NAMESPACE=${STACKSMITH_NAMESPACE:?Please provide the STACKSMITH_NAMESPACE environment variable.}
readonly port=8551


ensure_auth() {
  local redirect="http%3A%2F%2Flocalhost%3A${port}"
  local url="${STACKSMITH_API_URL}authn/oauth2/authorize?redirect_uri=${redirect}"
  if [ -z "${STACKSMITH_AUTH_MACAROON}" ]; then
    (sleep 2 && python -m webbrowser "${url}" > /dev/null 2>&1 ||
       echo "Please open this URL in your browser: ${url}") &
  fi
}

ensure_build() {
  docker build -q -t stacksmith-samples . > /dev/null 2>&1
}

exec_sample() {
  docker \
    run -v $PWD:/app \
    -p 8551:8551 \
    -e STACKSMITH_API_URL=$STACKSMITH_API_URL \
    -e STACKSMITH_NAMESPACE=$STACKSMITH_NAMESPACE \
    -e STACKSMITH_AUTH_MACAROON=$STACKSMITH_AUTH_MACAROON \
    -it stacksmith-samples python $@
}

main() {
  if [ $# -eq 0 ]; then
    echo "You must provide an example to run." 1>&2
    exit 1
  fi

  ensure_build
  ensure_auth
  exec_sample $@
}

main $@
