#!/bin/bash
# set up gunicorn for local development


target_dir="/home/tech-server/craftdot"
current_dir="$(pwd)"

# Check if the current directory is the target directory
if [ "$current_dir" != "$target_dir" ]; then
    cd "$target_dir"
    echo "Changed directory to $target_dir"
else
    echo "Already in $target_dir"
fi

# Activate the virtual environment
source .venv/bin/activate

# Create Gunicorn neccessary files
sudo mkdir -p "/var/log/gunicorn" "/var/run/gunicorn"
sudo chmod -R 777 "/var/log/gunicorn" "/var/run/gunicorn"
sudo chown -R www-data:www-data "/var/log/gunicorn" "/var/run/gunicorn"

# Run Gunicorn with the conf file 
gunicorn -c craftdot_api_gunicorn_conf.py api.v1.app:app > gunicorn_api.log &
gunicorn -c craftdot_frontend_gunicorn_conf.py frontend.app:app > gunicorn_frontend.log &
sudo tail -f /var/log/gunicorn/craftdot_frontend_access.log /var/log/gunicorn/craftdot_frontend_error.log > gunicorn_frontend.log &
sudo tail -f /var/log/gunicorn/craftdot_api_access.log /var/log/gunicorn/craftdot_api_error.log > gunicorn_api.log &


