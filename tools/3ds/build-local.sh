#!/bin/sh
# Builds 3DS homebrew inside the devkitpro/devkitarm Docker image, the same
# one GitHub Actions uses. For the Claude Code cloud sessions: the devkitPro
# package servers block these machines (Cloudflare), so devkitPro cannot be
# installed directly, but Docker Hub works.
#
# Usage, from the project directory:
#   tools/3ds/build-local.sh make TARGET=... EXTRA_CFLAGS="..."
#   tools/3ds/build-local.sh sh -c "cmake -B build ... && cmake --build build"
set -eu

if ! docker info >/dev/null 2>&1; then
    (dockerd >/tmp/dockerd.log 2>&1 &)
    i=0
    until docker info >/dev/null 2>&1; do
        i=$((i + 1))
        [ "$i" -gt 30 ] && { echo "dockerd did not start (see /tmp/dockerd.log)"; exit 1; }
        sleep 1
    done
fi

docker image inspect devkitpro/devkitarm:latest >/dev/null 2>&1 \
    || docker pull -q devkitpro/devkitarm:latest

exec docker run --rm -v "$PWD":/src -w /src devkitpro/devkitarm:latest "$@"
