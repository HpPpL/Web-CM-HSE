# Web-CM-HSE

**Команда для сборки:**

```shell
docker build -t web-ud .
```

**Команда для запуска веб-сервиса:**

```shell
docker run -d -p 80:5000 --mount type=bind,source=C:\Users\ender\Desktop\kal\pythonProject\temp-data,target=/app/temp-data --mount type=bind,source=C:\Users\ender\Desktop\kal\pythonProject\test-real-data,target=/app/test-real-data web-ud
```

**Команда для добавления пользователя веб-сервиса:**

```shell
docker exec -it <CONTAINER_NAME> python add-user.py
```