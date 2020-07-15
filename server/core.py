import os
from pathlib import Path
import numpy as np
from PIL import Image
import requests
from google.cloud import storage
import base64
from io import BytesIO
import uuid

__all__ = ['do', 'recaptcha_check']

def predict_and2jpg(model, cap):
    ''' cap: "white hair yellow eyes", returns: jpeg file buffer remember to close it or use with '''
    img, _ = model.predict(cap)
    img = Image.fromarray(np.uint8(img.numpy()))
    buf = BytesIO()
    img.save(buf, format='JPEG')
    buf.seek(0)
    return buf
# import matplotlib.pyplot as plt
# from deep_t2i.model_anime_heads import ExportedModel
# from deep_t2i.inference_anime_heads import predict
# model = ExportedModel.from_pretrained('./anime_heads.pt')
# with predict_and2jpg(model, "white hair yellow eyes") as buf:
#     img = Image.open(buf)
#     plt.imshow(img)
#     plt.show()


gs_bucket_id = os.getenv('gs_bucket_id')
def upload_to_gs(client, img_file):
    "upload img_file to google storage name it fname and return url"
    bucket = client.bucket(gs_bucket_id)
    fname = f'{uuid.uuid4().hex[:8]}.jpg'
    blob = bucket.blob(fname)
    blob.upload_from_file(img_file, content_type="image/jpeg")
    return f'https://storage.googleapis.com/{gs_bucket_id}/{fname}'
# from deep_t2i.model_anime_heads import ExportedModel
# from deep_t2i.inference_anime_heads import predict
# gs_client = storage.Client()
# model = ExportedModel.from_pretrained('./anime_heads.pt')
# with predict_and2jpg(model, "white hair yellow eyes") as buf:
#     url = upload_to_gs(gs_client, buf)
#     print(url)


imgur_client_id = os.getenv('imgur_client_id')
def upload_to_imgur(img_file):
    "upload img_file to imgur and return url"
    img = img_file.read()
    img = base64.standard_b64encode(img)
    url = "https://api.imgur.com/3/image"
    data = {'image': img, 'type': 'base64'}
    headers = { 'Authorization': f'Client-ID {imgur_client_id}' }
    res = requests.post(url, headers=headers, data=data).json()
    if res['success']: return res["data"]["link"]
    else: 
        raise Exception("Failed to upload to imgur")
# from deep_t2i.model_anime_heads import ExportedModel
# from deep_t2i.inference_anime_heads import predict
# model = ExportedModel.from_pretrained('./anime_heads.pt')
# with predict_and2jpg(model, "white hair yellow eyes") as buf:
#     url = upload_to_imgur(buf)
#     print(url)

def save_to_tmp(img_file):
    " save img_file to ./tmp_jpg/ "
    img = Image.open(img_file)
    fname = f'{uuid.uuid4().hex[:8]}.jpg'
    path = f'./temp_jpg/{fname}'
    img.save(path)
    return path
# from deep_t2i.model_anime_heads import ExportedModel
# from deep_t2i.inference_anime_heads import predict
# model = ExportedModel.from_pretrained('./anime_heads.pt')
# with predict_and2jpg(model, "white hair yellow eyes") as buf:
#     url = save_to_tmp(buf)
#     print(url)

img_server = os.getenv("img_server")
gs_client = storage.Client() if img_server=="gs" else None
def do(model, cap):
    "generate image from model, upload image to img_server and return link"
    with predict_and2jpg(model, cap) as buf:
        if img_server=="gs":
            url = upload_to_gs(gs_client, buf)
        elif img_server=="imgur":
            url = upload_to_imgur(buf)
        else:
            url = save_to_tmp(buf)
        return url


# Recaptcha check
recaptcha_secret = os.getenv('recaptcha_secret')
def recaptcha_check(token):
    if token is None: return False
    url = "https://www.google.com/recaptcha/api/siteverify"
    data = {
        'secret': recaptcha_secret,
        'response': token,
    }
    r = requests.post(url=url, data=data) 
    return r.json()['success']
