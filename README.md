# FastAPI Demo

## NGINX

```shell
echo "127.0.0.1 fastapi.aurora.inf" >> /etc/hosts
```

## STARTER

```bash
# main.py
python main.py

# uvicorn
uvicorn main:app --host 0.0.0.0 --port 8080

# hypercorn for http/2
hypercorn main:app --bind 0.0.0.0:8080

# gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### docker

```shell
make dev
```

### k8s

```shell
make prod
```

## ACCESS

http://fastapi.aurora.inf/
