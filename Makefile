export DOCKERFILE=docker/Dockerfile

run:
	docker stop covid19viz_01;
	docker rm covid19viz_01;
	docker build -f $(DOCKERFILE) -t neveldo/covid19viz:1.0 . && docker run -d -p 5000:5000 --name covid19viz_01 neveldo/covid19viz:1.0