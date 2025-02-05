# Aula sobre mensageria

## Iniciar o broker (Mosquitto) com docker:

```bash
docker run -d --name aula-mqtt -p 1883:1883 -p 9001:9001 eclipse-mosquitto:latest
```

## Inicia a API
```
uvicorn src.main:app --reload
```