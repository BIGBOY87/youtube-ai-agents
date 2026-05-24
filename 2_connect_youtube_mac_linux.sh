#!/usr/bin/env bash
set -e
if [ ! -f client_secret.json ]; then
  echo "ERROR: Missing client_secret.json"
  echo "Put the Google OAuth Desktop JSON file in this folder and rename it to client_secret.json"
  exit 1
fi
python3 main.py setup
