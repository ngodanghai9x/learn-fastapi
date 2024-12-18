# Template fastapi
- Common (utils, constants, configs, types) > Entities (DB ...) > Core Modules (email, logger) > Feature Modules (auth, user, product, order)

## Install
### Conda
- Install & create & activate env
- Python 3.12.7
### Packages
```sh
# pip install pip-tools
# pip-compile requirements.in
pip install -r requirements.txt
```

## Running app
```sh
make dev

make run
```

## Migration
To init alembic, run this command:
```bash
alembic init alembic
```
Then change config on `alembic.ini`, `alembic/env.py` 

(Hint: ```sqlalchemy.url, target_metadata, connectable (run_migrations_online)```)

To create a new migration, run this command (replacing the message as needed):
```bash
alembic revision --autogenerate -m "Add jsonb column to user"

alembic upgrade head

alembic downgrade -1
```