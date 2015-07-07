#!/bin/bash

echo "starting command"
echo $$ > $2/server-$1.pid
exec python -m SimpleHTTPServer $1
echo "stopping"
