#!/bin/bash


kill -TERM $(cat scripts/server-$1.pid)
rm scripts/server-$1.pid
