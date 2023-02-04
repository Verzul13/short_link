###### ПОДКЛЮЧЕНИЕ К REDIS
sudo docker exec -it ecy_redis_1 sh
redis-cli -a password123
keys *

celery -A config.celery_app --result-backend=redis://default:password123@0.0.0.0:6379/0 flower --port=5566

###### ПОДКЛЮЧЕНИЕ К MySQL
docker exec -it debd9261542f mysql -u root -p linkshortener
SHOW DATABASES;
USE test_db;
SHOW TABLES;

###### Создаль суперпользователя
    docker-compose run --rm django python manage.py createsuperuser
