import os
from flask import Flask, request

from deep_t2i.model import Anime_Export as AnimeHeadsModel, Birds_Export as BirdsModel
from deep_t2i.inference_anime_heads import predict
from deep_t2i.inference_birds import predict
from core import do, recaptcha_check

print("Env Var: ", os.environ)

app = Flask(__name__)
anime_heads_model = AnimeHeadsModel.from_pretrained('./anime_heads.pt')
birds_model = BirdsModel.from_pretrained('./birds.pt')


cors_options_res = ('', 204, {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600'
})
cors_header = {
    'Access-Control-Allow-Origin': '*'
}

@app.route('/anime_heads', methods=['POST', 'OPTIONS'])
def anime_heads_entry(supports_credentials=True):
    """
        request: 
            {
                "token": Recaptcha token,
                "cap": "white hair yellow eyes",
            }
        returns:
            An image url like: https://storage.cloud.google.com/deep_t2i_server/17cb0963.jpg or https://i.imgur.com/JdDDyfr.jpg
    """
    if request.method == 'OPTIONS':
        return cors_options_res
    print("enter anime_heads")

    # Parse request
    req = request.get_json(force=True)
    token = req.get('token', None)
    cap = req.get('cap', None)

    # recaptcha check
    if os.getenv('is_recaptcha')=='True' and not recaptcha_check(token):
        return ('Recaptcha failed!!!', 400, cors_header)

    # predict and upload image
    url = do(anime_heads_model, cap)
    print(f'mode: Anime_Heads, cap: {cap}, url: {url}')
    return (url, 200, cors_header)

@app.route('/birds', methods=['POST', 'OPTIONS'])
def birds_entry():
    """
        request: 
            {
                "token": Recaptcha token,
                "cap": "this is a white bird with a grey cheek patch and a black eyebrow.",
            }
        returns:
            An image url like: https://storage.cloud.google.com/deep_t2i_server/17cb0963.jpg or https://i.imgur.com/JdDDyfr.jpg
    """
    if request.method == 'OPTIONS':
        return cors_options_res
    print("enter birds")

    # Parse request
    req = request.get_json(force=True)
    token = req.get('token', None)
    cap = req.get('cap', None)

    # recaptcha check
    if os.getenv('is_recaptcha')=='True' and not recaptcha_check(token):
        return ('Recaptcha failed!!!', 400, cors_header)

    # predict and upload image
    url = do(birds_model, cap)
    print(f'mode: Birds, cap: {cap}, url: {url}')
    return (url, 200, cors_header)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('app_port', 5000)))

# def execute_req(mode, cap, headers):
#     # handle mode
#     if mode == 'anime_heads':
#         url = do(anime_heads_model, cap)
#         print(f'mode: {mode}, cap: {cap}, url: {url}')
#         return (url, 200, headers)
#     elif mode == 'birds':
#         url = do(birds_model, cap)
#         print(f'mode: {mode}, cap: {cap}, url: {url}')
#         return (url, 200, headers)
#     else:
#         return ('No such mode', 400, headers)


# def entry(request):
#     """
#         request: 
#             {
#                 "token": Recaptcha token,
#                 "mode": "anime_heads",
#                 "cap": "white hair yellow eyes",
#             }
#             {
#                 "token": Recaptcha token,
#                 "mode": "birds",
#                 "cap": "this is a white bird with a grey cheek patch and a black eyebrow.",
#             }
#         returns:
#             An image url like: https://storage.cloud.google.com/deep_t2i_server/17cb0963.jpg or https://i.imgur.com/JdDDyfr.jpg
#     """

#     # CORS
#     if request.method == 'OPTIONS':
#         headers = {
#             'Access-Control-Allow-Origin': '*',
#             'Access-Control-Allow-Methods': 'GET',
#             'Access-Control-Allow-Headers': 'Content-Type',
#             'Access-Control-Max-Age': '3600'
#         }
#         return ('', 204, headers)
#     headers = {
#         'Access-Control-Allow-Origin': '*'
#     }

#     # Parse request
#     req = request.get_json(force=True)
#     token = req.get('token', None)
#     mode = req.get('mode', None)
#     cap = req.get('cap', None)
#     if mode is None or cap is None: return ('Request Wrong!!', 400, headers)

#     # recaptcha check
#     if os.getenv('is_recaptcha')=='True' and not recaptcha_check(token):
#         return ('Recaptcha failed!!!', 400, headers)

#     try:
#         return execute_req(mode, cap, headers)
#     except Exception as e:
#         return (str(e), 500, headers)

 
# @app.route('/entry', methods=['GET', 'POST', 'OPTIONS'])
# def test_entry():
#     return entry(request)
