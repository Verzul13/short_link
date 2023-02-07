###### Главная страница
    http://0.0.0.0/main_page/

###### Swagger
    http://0.0.0.0/api/swagger/

###### Админка
    http://0.0.0.0/system/admin/

###### Prometheus
    http://0.0.0.0:9091

###### Grafana
    http://0.0.0.0:3000
    login: admin
    password: 9uT46ZKE

###### Создать суперпользователя
    docker-compose run --rm django python manage.py createsuperuser

###### Запуск тестов
    docker-compose run --rm django python manage.py test

**логи находятся в папке logs главной дирректории

**P.S. Папка .envs находится в репозитории для удобства поднятия контейнеров проверяющим.
В разработке такого делать нельзя, нужно использовать secrets