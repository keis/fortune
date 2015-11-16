#!/bin/bash

if echo "${FORTUNES}" | grep -qE '^s3://'; then
    aws s3 cp ${FORTUNES} /tmp/fortunes
else
    wget "${FORTUNES}" -O /tmp/fortunes
fi
exec python /fortune.py /tmp/fortunes
