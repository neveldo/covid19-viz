run-dev:
	-docker stop covid19viz_dev_01
	-docker rm covid19viz_dev_01
	docker build -f docker/dev/Dockerfile -t neveldo/covid19viz-dev:1.0 .
	docker run -d -p 5000:5000 --name covid19viz_dev_01 neveldo/covid19viz-dev:1.0

run-prod:
	-docker stop covid19viz_prod_01;
	-docker rm covid19viz_prod_01;
	docker build -f docker/prod/Dockerfile -t neveldo/covid19viz-prod:1.0 .
	docker run -d -p 80:80 --name covid19viz_prod_01 neveldo/covid19viz-prod:1.0