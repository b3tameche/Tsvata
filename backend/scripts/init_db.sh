# connect to the server and create database 'fastapi' if it doesn't exist
psql -U postgres << EOF
  SELECT 'CREATE DATABASE fastapi'
  WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'fastapi')\gexec
EOF
