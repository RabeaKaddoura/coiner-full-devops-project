#!/bin/sh


if [ -n "$VITE_API_URL" ]; then #checks system env variable. Set by frontend kubernetes deployment
    echo "Injecting VITE_API_URL: $VITE_API_URL"
    find /usr/share/nginx/html -type f -name "*.js" -exec sed -i "s|__VITE_API_URL__|$VITE_API_URL|g" {} \; #replaces the api url inside the production api.js with the system env variable value
else
    echo "Warning: VITE_API_URL not set"
fi

#execute the CMD
exec "$@"