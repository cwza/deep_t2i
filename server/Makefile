gcloud-login:
	gcloud auth application-default login

test:
	python -m unittest

run:
	env FLASK_APP=main.py flask run

curl-test:
	curl --header "Content-Type: application/json" \
		--request POST \
		--data '{"mode":"anime_heads","cap":"white hair yellow eyes"}' \
		http://127.0.0.1:5000/entry
deploy:
	gcloud functions deploy deep_t2i_server --entry-point entry \
		--runtime python37 --trigger-http --max-instances 1 --memory 1GB --allow-unauthenticated --env-vars-file .env.yaml
