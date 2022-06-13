SHELL=bash


run_app:
	@scripts/get_creds.sh
	@docker-compose up --build

 