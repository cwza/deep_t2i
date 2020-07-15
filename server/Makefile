gcloud-login:
	gcloud auth application-default login

curl-test:
	curl --header "Content-Type: application/json" \
		--request POST \
		--data '{"cap":"white hair yellow eyes"}' \
		http://127.0.0.1:${app_port}/anime_heads

docker-build:
	docker build -t us.gcr.io/play-263208/deep_t2i_server .

docker-run:
	docker run -p 5000:${app_port} --env-file .dockerenv us.gcr.io/play-263208/deep_t2i_server

deploy-docker:
	docker push us.gcr.io/play-263208/deep_t2i_server

deploy-gcloud-run:
	gcloud beta run services replace gcloud_service.yaml --platform managed --region us-central1
	# gcloud beta run services add-iam-policy-binding deep-t2i-server --member=allUsers --role=roles/run.invoker