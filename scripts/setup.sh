#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
STACK="$ROOT/vendor/wazuh-docker"
VERSION=v4.14.10

command -v docker >/dev/null 2>&1 || { echo "Docker is required." >&2; exit 1; }
docker compose version >/dev/null 2>&1 || { echo "Docker Compose is required." >&2; exit 1; }
command -v git >/dev/null 2>&1 || { echo "Git is required for the official Wazuh deployment files." >&2; exit 1; }

if [ ! -d "$STACK/.git" ]; then
  mkdir -p "$ROOT/vendor"
  git clone --depth 1 --branch "$VERSION" https://github.com/wazuh/wazuh-docker.git "$STACK"
fi

MANAGER_CONF="$STACK/single-node/config/wazuh_cluster/wazuh_manager.conf"
RULES="$ROOT/config/wazuh/rules/local_rules.xml"
[ -f "$MANAGER_CONF" ] || { echo "Expected Wazuh manager config was not found: $MANAGER_CONF" >&2; exit 1; }

python3 "$ROOT/scripts/prepare_wazuh.py" "$MANAGER_CONF"

cd "$STACK/single-node"
chmod -R u+rwX,go-rwx config/wazuh_indexer_ssl_certs
docker compose -f generate-indexer-certs.yml run --rm generator
if [ ! -f config/wazuh_indexer_ssl_certs/root-ca-manager.pem ] && [ -f config/wazuh_indexer_ssl_certs/root-ca.pem ]; then
  cp config/wazuh_indexer_ssl_certs/root-ca.pem config/wazuh_indexer_ssl_certs/root-ca-manager.pem
  chmod 600 config/wazuh_indexer_ssl_certs/root-ca-manager.pem
fi
if [ ! -f config/wazuh_indexer_ssl_certs/root-ca-manager.pem ]; then
  echo "Wazuh certificate generation did not produce root-ca-manager.pem." >&2
  exit 1
fi
cd "$ROOT"
docker compose -p lab5 -f vendor/wazuh-docker/single-node/docker-compose.yml -f docker-compose.lab5.yml up -d

echo "Lab stack started. Dashboard: https://localhost (admin / SecretPassword)"
echo "Replay the five synthetic scenarios with: python3 scripts/replay_scenarios.py"
