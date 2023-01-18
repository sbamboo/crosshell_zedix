#!/usr/bin/env bash
script_dir=$(dirname $(readlink -f $0))
script_dir="$script_dir/../crosshell.py"
python3 `echo $script_dir | tr -d '\r'` "$@"