#!/bin/bash

aws s3 cp ${FORTUNES} /tmp/fortunes
exec python /fortune.py /tmp/fortunes
