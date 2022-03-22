##
#  Payment Service
#
# @file
# @version 0.1

install:
	poetry install

run:
	uvicorn payment_service.main:app --reload

db_upgrade:
	alembic -c payment_service/migrations/alembic.ini upgrade head

# end
