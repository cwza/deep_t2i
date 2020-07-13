import os
from flask import Flask, request

from deep_t2i.model_anime_heads import ExportedModel as AnimeHeadsModel
from deep_t2i.inference_anime_heads import pred_and_show
from deep_t2i.model_birds import ExportedModel as BirdsModel
from deep_t2i.inference_birds import pred_and_show
from core import do, recaptcha_check

print("Env Var: ", os.environ)

app = Flask(__name__)
anime_heads_model = AnimeHeadsModel.from_pretrained('./anime_heads.pt')
birds_model = BirdsModel.from_pretrained('./birds.pt')


def execute_req(mode, cap, headers):
    # handle mode
    if mode == 'anime_heads':
        url = do(anime_heads_model, cap)
        print(f'mode: {mode}, cap: {cap}, url: {url}')
        return (url, 200, headers)
    elif mode == 'birds':
        url = do(birds_model, cap)
        print(f'mode: {mode}, cap: {cap}, url: {url}')
        return (url, 200, headers)
    else:
        return ('No such mode', 400, headers)


def entry(request):
    """
        request: 
            {
                "token": Recaptcha token,
                "mode": "anime_heads",
                "cap": "white hair yellow eyes",
            }
            {
                "token": Recaptcha token,
                "mode": "birds",
                "cap": "this is a white bird with a grey cheek patch and a black eyebrow.",
            }
        returns:
            An image url like: https://storage.cloud.google.com/deep_t2i_server/17cb0963.jpg or https://i.imgur.com/JdDDyfr.jpg
    """

    # CORS
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    # Parse request
    req = request.get_json(force=True)
    token = req.get('token', None)
    mode = req.get('mode', None)
    cap = req.get('cap', None)
    if mode is None or cap is None: return ('Request Wrong!!', 400, headers)

    # recaptcha check
    if os.getenv('is_recaptcha')=='True' and not recaptcha_check(token):
        return ('Recaptcha failed!!!', 400, headers)

    try:
        return execute_req(mode, cap, headers)
    except Exception as e:
        return (str(e), 500, headers)

 
@app.route('/entry', methods=['GET', 'POST', 'OPTIONS'])
def test_entry():
    return entry(request)

