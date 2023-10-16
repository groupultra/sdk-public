# Will remove everything from the current redis
# Be careful with this script

#!/bin/bash

# Your Redis password
redis_password=$(grep "REDIS_PASSWORD =" config.py | cut -d'=' -f2 | tr -d ' "' | tr -d ',')

# Get the Docker container ID for Redis
container_id=$(sudo docker ps | grep 'redis' | awk '{print $1}')

# Function to delete keys except those with service_id
function clear_redis_except_service_id {
    # Get the list of keys from Redis
    keys=$(sudo docker exec $container_id redis-cli -a $redis_password KEYS '*')
    
    # Iterate over the keys
    for key in $keys; do
        # Check if the key doesn't contain service_id
        if [[ $key != *"service_id"* ]]; then
            # Delete the key
            sudo docker exec $container_id redis-cli -a $redis_password DEL "$key"
        fi
    done
}

# Run the function
clear_redis_except_service_id



