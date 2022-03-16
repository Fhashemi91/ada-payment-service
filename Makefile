##
#  Finance Service
#
# @file
# @version 0.1

install:
	poetry install

run:
	uvicorn finance_service.main:app --reload

db_upgrade:
	alembic -c finance_service/migrations/alembic.ini upgrade head

# end
