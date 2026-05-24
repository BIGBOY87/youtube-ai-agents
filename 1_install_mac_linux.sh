#!/usr/bin/env bash
set -e
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
echo "Done. Next: put client_secret.json in this folder, then run bash 2_connect_youtube_mac_linux.sh"
