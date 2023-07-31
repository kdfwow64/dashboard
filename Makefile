build_for_dev_prod:
	DOCKER_BUILDKIT=1 docker build \
		-t django-dashboard \
		--secret id=aws,src=credentials .

build:
	docker build \
		--platform linux/amd64 \
		-t django-dashboard \
    	--secret id=aws,src=credentials .


run:
	docker run -d -p 5000:5000 \
	-v $$HOME/.aws/credentials:/root/.aws/credentials:ro \
	--env "AWS_PROFILE=default" \
	--env "AWS_DEFAULT_REGION=us-east-1" \
	--name django-dashboard django-dashboard

deploy:
	make remove -k
	make build
	make run

remove:
	docker rm django-dashboard -f

restart:
	make remove
	make deploy

deploy_to_dev:
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 238988874017.dkr.ecr.us-east-1.amazonaws.com
	make build_for_dev_prod
	docker tag django-dashboard 238988874017.dkr.ecr.us-east-1.amazonaws.com/django-dashboard:latest
	docker push 238988874017.dkr.ecr.us-east-1.amazonaws.com/django-dashboard:latest
	make update_ecs_docker_dev

update_ecs_docker_dev:
	aws ecs update-service --cluster django-dashboard --service django-dashboard-svc --force-new-deployment --region us-east-1

deploy_to_prod:
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 467911368405.dkr.ecr.us-east-1.amazonaws.com
	make build_for_dev_prod
	docker tag django-dashboard 467911368405.dkr.ecr.us-east-1.amazonaws.com/django-dashboard:latest
	docker push 467911368405.dkr.ecr.us-east-1.amazonaws.com/django-dashboard:latest
	make update_ecs_docker_prod

update_ecs_docker_prod:
	aws ecs update-service --cluster django-dashboard --service django-dashboard-prod-svc --force-new-deployment --region us-east-1
