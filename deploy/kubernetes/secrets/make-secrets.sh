#!/usr/bin/env bash

postgres_password=$(head -c 512 /dev/urandom | LC_CTYPE=C tr -cd 'a-zA-Z0-9' | head -c 32)

cat <<EOF >> postgres-secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: postgres-secret
  namespace: sgh
type: kubernetes.io/basic-auth
stringData:
  username: sgh
  password: $postgres_password
---
apiVersion: v1
kind: Secret
metadata:
  name: postgres-url-secret
  namespace: sgh
stringData:
  url: postgresql://sgh:$postgres_password@postgres-cluster-rw.sgh.svc/sgh_production
EOF

jwt_secret=$(head -c 512 /dev/urandom | LC_CTYPE=C tr -cd 'a-zA-Z0-9' | head -c 64)

cat <<EOF >> jwt-secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: jwt-secret
  namespace: sgh
stringData:
  secret: $jwt_secret
EOF
