# TODO app (Technical Task)

## Dependencies

- [poetry](https://python-poetry.org/docs/#installing-manually)
- [docker](https://docs.docker.com/get-docker/)

### requirements.txt (run before build images)

```shell
 poetry export -f requirements.txt --output requirements.txt --without-hashes
```

### Build

```shell
docker-compose -f .\docker\compose\docker-compose.local.yml -p todo build

# or
docker build -f .\docker\django\Dockerfile -t todo-app:dev .

# or
make build
```

### Start

```shell
docker-compose -f .\docker\compose\docker-compose.local.yml -p todo up -d

# or
make up
```

### Note

After starting the containers,
it'll create default superuser with such credentials:

- login `super-admin@example.com`
- password `super-admin123`

### For testing email sending fill in the following environment variables in `/docker/environment/app.local.env`:
- EMAIL_HOST_USER
- [**EMAIL_HOST_PASSWORD**](https://support.google.com/accounts/answer/185833?hl=en)

