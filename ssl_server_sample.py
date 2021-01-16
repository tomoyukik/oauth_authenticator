# https://qiita.com/masakielastic/items/05cd6a36bb6fb10fccf6
#    httpsサーバ
# https://qiita.com/kai_kou/items/d03abd6012f32071c1aa
#    OAuth トークン取得
# https://qiita.com/miriwo/items/3a19b92dd0c77e6d2378
#     証明書のせいでchromeでひらけない
# https://developers-book.com/2020/09/24/302/
#     自己証明書エラー　verify fale
# https://booth.pm/ja/items/1296585 
#    OAuth
# http://ja.pymotw.com/2/SocketServer/
#   serve_foreverは無限ループ
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import ssl

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import urlopen, HTTPError
from webbrowser import open_new
import json
import random, string
import urllib.parse
import urllib.request

MAUTIC_API_BASE_URL = 'https://0.0.0.0'
CLIENT_ID = '1_5j8ecbsu9cowo4wk8kwwcc8k8wc08c8o4sgo4s084cg880ggo0'
CLIENT_SECRET = '172h8p6mevy8w8cggc44gw4w4ookk4ockg440osggkw808c00g'

class AuthenticationHandler(BaseHTTPRequestHandler):
    def __init__(self, request, address, server, client_id, client_secret):
        print('init')
        self._client_id = client_id
        self._client_secret = client_secret
        super().__init__(request, address, server)

    def do_GET(self):
        print('do_GET called!!')
        print(self.path)
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        print(params['code'][0], params['state'][0])

        self.__responde()

        if 'code' in self.path:
            self.server.access_token = None

            response = self._send_post_request()
            print('response_status code:', response.status_code)
            print('response content:', response.content)
            if response.status_code == 200:
                print('response json:', response.json)
                self.server.access_token = response.json()['access_token']

            self.wfile.write(bytes('sorry', 'utf-8'))
            return
            
        self.wfile.write(bytes('gomengo', 'utf-8'))
        return

    def __responde(self):
        self.send_response(200)
        self.end_headers()

    def _join_url(self, base_url, sub_directory, params):
        params_joined = '&'.join(['='.join(p) for p in params.items()])
        joined_url = ''.join([base_url, sub_directory])
        return '?'.join([joined_url, params_joined])

    def _send_post_request(self):
        params = self.path.split('&')
        state = params[0].replace('/?state=', '')
        code = params[1].replace('code=', '')

        access_url = f'{MAUTIC_API_BASE_URL}/oauth/v2/token'
        headers = {'Content-Type': 'application/json'}
        params = {
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'grant_type': 'authorization_code',
            'redirect_uri': 'https://0.0.0.0:8888',
            'code': code
        }
        response = requests.post(access_url, data=params, verify=False)
        return response

class AccessTokenHandler:

    def __init__(self, client_id, client_secret):
        self._client_id = client_id
        self._client_secret = client_secret

    def get_access_token(self):
        token = None
        host = '0.0.0.0'
        port = 8888
        grant_type = 'authorization_code'
        app_url = 'https://0.0.0.0:8888'
        response_type = 'code'
        authorize_path = '/oauth/v2/authorize'

        handler = lambda request, address, server: AuthenticationHandler(
            request, address, server, CLIENT_ID, CLIENT_SECRET
        )

        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain('./ssl_test.crt', keyfile='./ssl_test.key')
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1

        params = {
            'client_id': CLIENT_ID,
            'grant_type': grant_type,
            'redirect_uri': urllib.parse.quote(app_url, safe=''),
            'response_type': response_type,
            'state': self._randomname(40)
        }
        access_url = self._join_url(MAUTIC_API_BASE_URL, authorize_path, params)
        open_new(access_url)

        with HTTPServer((host, port), handler) as server:
            server.socket = context.wrap_socket(server.socket)
            print('Server Starts - %s:%s' % (host, port))

            try:
                while token is None:
                    server.access_token = None
                    server.handle_request()
                    token = server.access_token
            except KeyboardInterrupt:
                pass

        print('アクセストークン取れたよー', token)
        print('Server Stops - %s:%s' % (host, port))
        return token


    def _randomname(self, n):
        randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
        return ''.join(randlst)

    def _join_url(self, base_url, sub_directory, params):
        params_joined = '&'.join(['='.join(p) for p in params.items()])
        joined_url = ''.join([base_url, sub_directory])
        return '?'.join([joined_url, params_joined])

# mauticにアクセス(GET リクエスト)
# サーバ起動
# レスポンスを取得
# POSTリクエスト
# レスポンス取得

if __name__ == '__main__':
    # get_access_token()
    handler = AccessTokenHandler(CLIENT_ID, CLIENT_SECRET)
    print('だから取れたぞー', handler.get_access_token())