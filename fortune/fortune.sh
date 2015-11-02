#!/bin/bash

aws s3 cp ${FORTUNES} /tmp/fortunes
python /fortune.py /tmp/fortunes
