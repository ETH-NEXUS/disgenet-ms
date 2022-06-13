#!/usr/bin/env bash

DISGENET_CREDS="app/.disgenet_creds"


if [ ! -f ${DISGENET_CREDS} ]; then
    echo "DISGENET datafiles require an account to download; first, register at https://www.disgenet.org/signup/"

    if [[ -t 0 ]]; then 
        echo "Once registered, enter your credentials below so they can be used to retrieve your file"
        read -p 'Email: ' DISGENET_USERNAME
        read -sp 'Password: ' DISGENET_PASSWORD
        echo
        echo "${DISGENET_USERNAME}:${DISGENET_PASSWORD}" | base64 > ${DISGENET_CREDS}
        echo "Your input has been stored to ${DISGENET_CREDS}, which you should treat as sensitive."
    else
        echo "Once registered, run the following command to store your credentials and re-run this script:"
        echo "echo 'email@example.com:mydisgenetpassword' | base64 > ${DISGENET_CREDS}"
        echo "(This file will contain your credentials, so treat it as sensitive.)"
        exit 1
    fi
fi