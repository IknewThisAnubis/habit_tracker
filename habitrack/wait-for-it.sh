#!/usr/bin/env bash
set -e

host="$1"
shift

python - <<EOF
import socket, time
host, port = "$host".split(":")
while True:
    try:
        with socket.create_connection((host, int(port)), timeout=1):
            break
    except OSError:
        time.sleep(1)
EOF

exec "$@"

