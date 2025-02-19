# wsl run commands

## virtual environment

```
source venv/bin/activate
```

### run the application

```
python main.py
```

### start redis

```
sudo service redis-server start
sudo service redis-server status
sudo service redis-server stop
```

### start celery worker

```
celery -A main:celery_app worker --loglevel INFO
```

### start celery beat

```
celery -A main:celery_app beat --loglevel INFO
```

### start mail server

```
~/go/bin/MailHog
```