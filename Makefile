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

deploy:
	gcloud builds submit --tag gcr.io/ada-return/payment-service
	gcloud run deploy --image gcr.io/ada-return/payment-service --platform managed

# end
