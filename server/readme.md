# Deep_t2i Demo Server Site
> Flask server that use the model generated from deep_t2i to generate image and upload it to image server

## Functionality
* Generate anime face image by machine. You can specify hair color and eye color.
* Generate bird image by machine. You can specify any string that describe the bird. 

## Environment Variables
``` sh
export img_server=gs or imgur or none
export gs_bucket_id=Your google cloud storage bucket id if you want to use cloud storage as your image server
export imgur_client_id=Your imgur client id if you want to use imgur as your image server
export is_recaptcha=True or False to enable or disable the recaptcha check
export recaptcha_secret=Your recaptcha secret if you want to use recaptcha
```

## Request Example
``` 
request: 
    {
        "token": Recaptcha token,
        "mode": "anime_heads",
        "cap": "white hair yellow eyes",
    }
    or
    {
        "token": Recaptcha token,
        "mode": "birds",
        "cap": "this is a white bird with a grey cheek patch and a black eyebrow.",
    }
response:
    An image url like: https://storage.googleapis.com/deep_t2i_server/17cb0963.jpg or https://i.imgur.com/JdDDyfr.jpg
```

## Run Dev Server
1. pip install -r requirements_local.txt
2. Generate anime_heads.pt and birds.pt from deep_t2i and put them inside this directory.
3. Correctly set up your image server(google cloud storage or imgur) and the according environment variables
4. Correctly set up recaptcha and the according environment variables
5. make run

## Simple Test
**Test Without Recaptcha**
1. Disable recaptcha by environment variable
2. make curl-test

**Test With Recaptcha**
1. Enable recaptcha by environment variable
2. Run recaptcha.html by any httpserver
3. Open recaptcha.html by browser
4. check the recaptcha box, click submit and see the developer console print the uploaded image url

## Deploy
* Correctly set up environment variables in .env.yaml
* make deploy 
* This command will deploy this service to google cloud function.
* It is best to create a service account that only with the cloud storage object creation privilege and attach it to this function. The default auth of cloud function is too powerful.
