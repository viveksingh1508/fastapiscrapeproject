alembic init

# to create migrations

alembic revision --autogenerate -m 'Create users table'

# to migrate tables

alembic upgrade head
