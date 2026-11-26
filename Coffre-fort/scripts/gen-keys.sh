#!/usr/bin/env bash
mkdir -p keys
openssl genpkey -algorithm Ed25519 -out keys/jwt_private.pem
openssl pkey -in keys/jwt_private.pem -pubout -out keys/jwt_public.pem
chmod 600 keys/jwt_private.pem
