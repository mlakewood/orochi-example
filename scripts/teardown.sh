#!/bin/bash


kill -TERM $(cat scripts/server.pid)
rm scripts/server.pid

