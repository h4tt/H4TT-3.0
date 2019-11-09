#!/bin/sh
set -eo pipefail

WORKERS=${WORKERS:-1}
WORKER_CLASS=${WORKER_CLASS:-gevent}
ACCESS_LOG=${ACCESS_LOG:--}
ERROR_LOG=${ERROR_LOG:--}
WORKER_TEMP_DIR=${WORKER_TEMP_DIR:-/dev/shm}

# Check that the database is available
if [ -n "$DATABASE_URL" ]
    then
    url=`echo $DATABASE_URL | awk -F[@//] '{print $4}'`
    database=`echo $url | awk -F[:] '{print $1}'`
    port=`echo $url | awk -F[:] '{print $2}'`
    echo "Waiting for $database:$port to be ready"
    while ! mysqladmin ping -h "$database" -P "$port" --silent; do
        # Show some progress
        echo -n '.';
        sleep 1;
    done
    echo "$database is ready"
    # Give it another second.
    sleep 1;
fi

# Initialize database
python manage.py db upgrade

python import.py /import/ctfd-import.zip