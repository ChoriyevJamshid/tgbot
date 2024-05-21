
set -o errexit
set -o nounset

until cd /app/backend
do
    echo "Waiting for server volume..."
done

celery -A djconfig worker --loglevel=info



