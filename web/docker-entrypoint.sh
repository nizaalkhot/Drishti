#!/bin/sh
set -e

# If VITE_API_BASE environment variable is provided, inject it into index.html for dynamic runtime resolution
if [ -n "$VITE_API_BASE" ]; then
    echo "Injecting runtime VITE_API_BASE=$VITE_API_BASE into index.html"
    sed -i "s|<head>|<head><script>window.__DRISHTI_API_BASE__ = \"$VITE_API_BASE\";</script>|g" /usr/share/nginx/html/index.html
fi

exec "$@"
