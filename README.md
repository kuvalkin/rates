# Rates

The repo contains solution to [HTTP API task](https://github.com/xeneta/ratestask).

## Quick start

```shell
git clone https://github.com/kuvalkin/rates
cd rates
docker compose up
```

The endpoint is available at `http://localhost:5000/rates`.

### Run tests
Assuming that you have `docker compose up` running and current working directory is
the repo.
```shell
docker compose exec app /bin/bash -c "pytest"
```

For more verbose output run
```shell
docker compose exec app /bin/bash -c "pytest -vv"
```

## About the code

- `db` service was taken from the [original repo](https://github.com/xeneta/ratestask) without changes.
- `.env` file is under version control, which is a bad practice generally. It is provided for demonstration purposes
and ease of setup.
- End-to-end tests should generally use a separated DB instance with predefined data. But since the `db` service is
exactly this — a DB instance with fixed data, I decided not to create a separate service. However, that should be 
considered if the situation changes.
