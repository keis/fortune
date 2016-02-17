#!/bin/bash

if test -n "${FORTUNES}"; then
    if echo "${FORTUNES}" | grep -qE '^s3://'; then
        aws s3 cp ${FORTUNES} /tmp/fortunes
    else
        wget "${FORTUNES}" -O /tmp/fortunes
    fi
fi
exec python /fortune.py /tmp/fortunes
