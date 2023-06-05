Инструкция по запуску сервера:

Подготовка Redis:

1. Обновите кэш пакетов apt:
- sudo apt update
2. Установите redis
- sudo apt install redis-server
3. Откройте файл конфигураций в любом редакторе (например nano)
- sudo nano /etc/redis/redis.conf
Найдите в нем директиву "supervised" и измените для нее значение с "no" на "systemd"
Сохраните изменения путем нажатия CTRL + X, Y и затем Enter
4. Перезапустите redis
- sudo systemctl restart redis.service

Подготовка проекта:

В терминале ubuntu создайте каталог для проекта и перейдите в него:
- mkdir notification_service && cd notification_service

Установите pip (если не установлено):
- sudo apt install -y python3-pip

Установите venv (если не установлено):
- sudo apt install -y python3-venv

Создайте виртуальное окружение:
- python3 -m venv env

Активируйте виртуальное окружение:
- source env/bin/activate

Клонируйте код из git репозитория:
- git clone https://github.com/serebas/notification_service.git

Установите в проект все зависимости:
- pip install -r requirements.txt

Примените существующие миграции:
- python3 manage.py migrate

Запустите сервер на локалхосте:
- python3 manage.py runserver

Откройте новое окно терминала и запустите сервер redis
- redis-server
Если получите ошибку о том что адрес уже используется, введите
- sudo service redis-server stop
и попытайтесь заустить сервер снова

Откройте еще одно окно терминала и запустите планировщик задач Celery с флагом -B для выполнения задач из расписания:
- celery -A notifications worker -B -l INFO (убедитесь что вы находитесь в каталоге проекта)

Для доступа к внешнему сервису уведомлений я использовал выданный Вами токен, но он лежит в переменной окружения которого нет в репозитории,
если что то вот он: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTU4Nzg4OTAsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6Imh0dHBzOi8vdC5tZS9hcnNoYXNjaGluZSJ9.RQKhmXOQtwWgkV-zcsw6z9qviyvcosxKTNQxaXkttSY
используется в файле distribution/tasks.py в 19 строке
