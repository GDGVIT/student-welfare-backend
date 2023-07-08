#!/bin/sh

# Student Welfare Backend
if [ $1 = "local" ]; then
    shift # Discard the first argument
    env="local"
    file="local.yml"
else
    env="production"
    file="production.yml"
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/student_welfare_backend/" && docker-compose -f "$file" "$@"