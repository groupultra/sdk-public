#!/bin/bash

# # 创建一个新的 tmux 会话，但不要附加到它
# tmux new-session -d -s python_session

# # 在 tmux 会话中执行 Python 脚本并将输出重定向到一个以时间命名的文件
# tmux send-keys -t python_session "python3 main.py 2>&1 | tee console_logs/$(date +\"%Y%m%d_%H%M%S\").log" C-m

# Get the value of DATABASE_TYPE from config.py
DATABASE_TYPE=$(grep "DATABASE_TYPE =" config.py | cut -d'=' -f2 | tr -d ' "' | tr -d ',')

if [ "$DATABASE_TYPE" == "json" ]; then
  echo "JSON DATABASE"
elif [ "$DATABASE_TYPE" == "redis" ]; then
  echo "REDIS DATABASE"
  redis_password=$(grep "REDIS_PASSWORD =" config.py | cut -d'=' -f2 | tr -d ' "' | tr -d ',')

  # redis_password=$(jq -r '.REDIS_PASSWORD' config.json)
  if [ -z "$redis_password" ]; then
      echo "Error: Password not found or empty in config.py"
      exit 1
  fi

  redis_session_name="redis_session"

  # Check if the session already exists
  tmux has-session -t $redis_session_name 2>/dev/null

  # $? is a special variable in bash that holds the exit status of the last command executed
  if [ $? != 0 ]; then
    # If the session does not exist, create a new session and run Redis server
    tmux new-session -d -s $redis_session_name
    echo "Started new session and running Redis server."
    tmux send-keys -t $redis_session_name "sudo docker run -d -p 6379:6379 redis redis-server --requirepass $redis_password" C-m
  else
    if ! pgrep -f "redis-server" > /dev/null; then
      # If Redis is not running, send the Docker command to the session
      tmux send-keys -t $redis_session_name "sudo docker run -d -p 6379:6379 redis redis-server --requirepass $redis_password" C-m
      echo "Session $redis_session_name exists but Redis isn't running. Running the Docker command."
    else
      echo "Session $redis_session_name exists and Redis is already running."
    fi
  fi


  while ! pgrep -f "redis-server" > /dev/null; do
      echo "Waiting for redis-server to start..."
      sleep 2 # Sleep for 2 seconds (you can adjust this value as needed)
  done


  # 如果你想自动附加到这个会话，可以取消下面这行的注释
  # tmux attach-session -t python_session
else
  echo "Error: Unknown value for DATABASE_TYPE in config.py"
  exit 1
fi

python_session_name="python_session"

tmux has-session -t $python_session_name 2>/dev/null

if [ $? != 0 ]; then
  # If the session does not exist, create a new session and run the Python script
  tmux new-session -d -s $python_session_name
  echo "Started new python session and running main python script."
  tmux send-keys -t $python_session_name "python3 main.py 2>&1 | tee console_logs/$(date +\"%Y%m%d_%H%M%S\").log" C-m
else
  # If the session exists, check if main.py is running within it
  is_running=$(tmux list-panes -t $python_session_name -F "#{pane_current_command}" | grep python3)

  if [ -z "$is_running" ]; then
    echo "Session $python_session_name exists but main.py isn't running. Running the main python script."
    tmux send-keys -t $python_session_name "python3 main.py 2>&1 | tee console_logs/$(date +\"%Y%m%d_%H%M%S\").log" C-m
  else
    echo "Session $python_session_name exists and main.py is already running."
  fi
fi