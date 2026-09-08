#!/usr/bin/env bash
# Run on the server after git pull (GitHub Actions SSH or manual).
set -euo pipefail

REPO="${DEPLOY_REPO_PATH:-/root/homepickdock.com}"
DOCROOT="${DEPLOY_DOCROOT_PATH:-}"

cd "${REPO}"
git fetch origin main
git reset --hard origin/main
echo "Pulled: $(git log -1 --oneline)"

if [ -z "${DOCROOT}" ]; then
  for candidate in \
    /home/*/domains/homepickdock.com/public_html \
    /home/*/homepickdock.com/public_html \
    /home/*/public_html; do
    for d in ${candidate}; do
      if [ -d "${d}" ]; then
        DOCROOT="${d}"
        break 2
      fi
    done
  done
fi

if [ -n "${DOCROOT}" ] && [ "${DOCROOT}" != "${REPO}" ]; then
  rsync -a --delete \
    --exclude '.git/' \
    --exclude 'scripts/__pycache__/' \
    "${REPO}/" "${DOCROOT}/"
  echo "Synced to ${DOCROOT}"
  LIVE_ROOT="${DOCROOT}"
else
  LIVE_ROOT="${REPO}"
fi

test -f "${LIVE_ROOT}/index.html"
echo "Deploy OK — homepage live at ${LIVE_ROOT}/index.html"
