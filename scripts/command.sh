#!/bin/bash

echo "starting command"
python -m SimpleHTTPServer $1  & echo $! > scripts/server.pid
echo "stopping"
