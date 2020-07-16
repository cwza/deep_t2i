# Deep_t2i Demo Server Site
> Flask server that use the model generated from deep_t2i to generate image and upload it to image server

## Functionality
* Generate anime face image by machine. You can specify hair color and eye color.
* Generate bird image by machine. You can specify any string that describe the bird. 

## Environment Variables
``` sh
export app_port=app port
export img_server=gs or imgur or none
export gs_bucket_id=Your google cloud storage bucket id if you want to use cloud storage as your image server
export imgur_client_id=Your imgur client id if you want to use imgur as your image server
export is_recaptcha=True or False to enable or disable the recaptcha check
export recaptcha_secret=Your recaptcha secret if you want to use recaptcha
```

## Request Example
``` 
POST to: http://127.0.0.1/anime_heads
request: 
    {
        "token": Recaptcha token,
        "cap": "white hair yellow eyes",
    }
response:
    An image url like: https://storage.googleapis.com/deep_t2i_server/17cb0963.jpg or https://i.imgur.com/JdDDyfr.jpg
```
```
POST to: http://127.0.0.1/birds
request: 
    {
        "token": Recaptcha token,
        "cap": "this is a white bird with a grey cheek patch and a black eyebrow.",
    }
response:
    An image url like: https://storage.googleapis.com/deep_t2i_server/17cb0963.jpg or https://i.imgur.com/JdDDyfr.jpg
```

## Run Dev Server
1. pip install -r requirements.txt
2. Generate anime_heads.pt and birds.pt from deep_t2i and put them inside this directory.
3. Correctly set up your image server(google cloud storage or imgur) and the according environment variables
4. Correctly set up recaptcha and the according environment variables
5. python app.py

## Simple Test
**Test Without Recaptcha**
1. Disable recaptcha by environment variable
2. make curl-test

**Test With Recaptcha**
1. Enable recaptcha by environment variable
2. Replace data-sitekey in recaptcha.html by yours
3. Run recaptcha.html by any httpserver
4. Open recaptcha.html by browser
5. check the recaptcha box, click submit and see the developer console print the uploaded image url

## Deploy
1. Generate gcloud_service.yaml but replace [] by yours.
``` yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: deep-t2i-server
spec:
  template:
    spec:
      containers:
      - image: us.gcr.io/[PROJECT_ID]/deep_t2i_server:latest
        resources:
          limits:
            cpu: '2'
            memory: '2G'
        ports:
        - containerPort: 5000
        env:
        - name: app_port
          value: '5000'
        - name: img_server
          value: [gs or imgur]
        - name: gs_bucket_id
          value: []
        - name: imgur_client_id
          value: []
        - name: is_recaptcha
          value: ['True' or 'False']
        - name: recaptcha_secret
          value: []
    metadata:
      annotations:
        autoscaling.knative.dev/maxScale: '2' 
```
3. Run followings but replace [] by yours.
``` sh
gcloud login
gcloud auth configure-docker
docker build -t us.gcr.io/[GCP_PROJECT_ID]/deep_t2i_server .
docker push us.gcr.io/[GCP_PROJECT_ID]/deep_t2i_server
gcloud beta run services replace gcloud_service.yaml --region us-central1
```
4. Add --member=allUsers --role=roles/run.invoker on the permissions of this app
4. It is best to create a service account that only with the cloud storage object creation privilege and attach it to this app. The default auth of cloud run is too powerful.