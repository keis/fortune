#!/bin/bash

exec python /cookie.py ${PORT:+--port "$PORT"}
