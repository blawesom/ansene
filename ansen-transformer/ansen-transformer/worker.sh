# sudo rabbitmqctl add_user myuser mypassword
# sudo rabbitmqctl add_vhost myvhost
# sudo rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"

export C_FORCE_ROOT=true
celery -A distributer worker --loglevel=info --concurrency=100