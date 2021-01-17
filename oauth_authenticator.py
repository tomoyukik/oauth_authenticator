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
from http.server import HTTPServer
import ssl

from webbrowser import open_new
import random
import string
import urllib.parse

from access_token_request_handler import AccessTokenRequestHandler

class OAuthAuthenticator:

    def __init__(self, client_credential, client_info, authorize_url):
        # クレデンシャル読み込み
        self._client_credential = client_credential
        self._client_info = client_info
        self._authorize_url = authorize_url
        self._authorization_result = None
        self._app_uri = 'https://%s:%s' % (client_info['host'], client_info['port'])
        # 証明書読み込み

    def get_access_token(self):
        token = None

        params = {
            'client_id': self._client_credential['id'],
            'grant_type': 'authorization_code',
            'redirect_uri': self._app_uri,
            'response_type': 'code',
            'state': self.__randomname(40)
        }
        access_url = urllib.parse.urljoin(self._authorize_url, 'authorize')
        access_url = '?'.join([access_url, urllib.parse.urlencode(params)])

        # 認可コードリクエスト
        self.__request_authorization_code(access_url)

        # トークンリクエスト
        handler = lambda request, address, server: AccessTokenRequestHandler(
            request, address, server, self._client_credential, self._app_uri, self._authorize_url
        )
        with HTTPServer((self._client_info['host'], self._client_info['port']), handler) as server:
            print('Server Starts - %s:%s' % (self._client_info['host'], self._client_info['port']))
            server.socket = self.__wrap_socket_ssl(server.socket)

            try:
                while token is None:
                    server.result = None
                    server.handle_request()
                    token = server.result
            except KeyboardInterrupt:
                pass

        print('Server Stops - %s:%s' % (self._client_info['host'], self._client_info['port']))

    def result(self):
        return self._authorization_result

    def __request_authorization_code(self, access_url):
        open_new(access_url)

    def __wrap_socket_ssl(self, socket):
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain('./ssl_test.crt', keyfile='./ssl_test.key')
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        return context.wrap_socket(socket)

    def __randomname(self, n):
        randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
        return ''.join(randlst)