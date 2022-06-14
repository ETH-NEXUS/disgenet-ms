deploy: .disgenet_creds
	@docker-compose up -d

redeploy: .disgenet_creds
	@git pull
	@docker-compose up -d --build

.disgenet_creds:
	@scripts/get_creds.sh

 