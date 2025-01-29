python manage.py migrate

if [ -d "fixtures" ] && [ "$(ls -A fixtures)" ]; then
    echo "Loading fixtures..."
    python manage.py loaddata fixtures/db.json
else
    echo "No fixtures to load."
fi

exec "$@"