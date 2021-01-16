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

class GetHandler(BaseHTTPRequestHandler):
    def __init__(self, request, address, server, client_id, client_secret):
        print('init')
        self._client_id = client_id
        self._client_secret = client_secret
        super().__init__(request, address, server)

    def do_GET(self):
        print('do_GET called!!')
        print(self.path)

        self.send_response(200)
        self.end_headers()

        if 'code' in self.path:
            params = self.path.split('&')
            state = params[0].replace('/?state=', '')
            code = params[1].replace('code=', '')
            url = f'{MAUTIC_API_BASE_URL}/oauth/v2/token'
            headers = {'Content-Type': 'application/json'}
            params = {
                'client_id': self._client_id,
                'client_secret': self._client_secret,
                'grant_type': 'authorization_code',
                'redirect_uri': 'https://0.0.0.0:8888',
                'code': code
            }
            response = requests.post(url, data=params, verify=False)
            self.server.access_token = None

            print('response_status code:', response.status_code)
            print('response content:', response.content)

            if response.status_code == 200:
                print('response json:', response.json)
                self.server.access_token = response.json()['access_token']

            self.wfile.write(bytes('sorry', 'utf-8'))
            return
            
        self.wfile.write(bytes('gomengo', 'utf-8'))
        return

def randomname(n):
    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    return ''.join(randlst)

def join_url(base_url, sub_directory, params):
    params_joined = '&'.join(['='.join(p) for p in params.items()])
    joined_url = ''.join([base_url, sub_directory])
    return '?'.join([joined_url, params_joined])


def run(host, port, ctx, handler):
    token = None

    params = {
        'client_id': CLIENT_ID,
        'grant_type': 'authorization_code',
        'redirect_uri': urllib.parse.quote('https://0.0.0.0:8888', safe=''),
        'response_type': 'code',
        'state': randomname(40)
    }
    access_url = join_url(MAUTIC_API_BASE_URL, '/oauth/v2/authorize', params)
    open_new(access_url)

    with HTTPServer((host, port), handler) as server:
        server.socket = ctx.wrap_socket(server.socket)
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

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 8888

    ssl._create_default_https_context = ssl._create_unverified_context
    ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ctx.load_cert_chain('./ssl_test.crt', keyfile='./ssl_test.key')
    ctx.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
    handler = lambda req, add, ser: GetHandler(req, add, ser, CLIENT_ID, CLIENT_SECRET)

    run(host, port, ctx, handler)