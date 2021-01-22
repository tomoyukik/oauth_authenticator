from http.server import HTTPServer
import ssl

from webbrowser import open_new
import random
import string
import urllib.parse

from access_token_request_handler import AccessTokenRequestHandler

class OAuthAuthenticator:

    def __init__(self, client_credential, client_info, auth_url):
        self.__client_credential = client_credential
        self.__client_info = client_info
        self.__host = client_info['host']
        self.__port = client_info['port']
        self.__authenticate_url = urllib.parse.urljoin(auth_url['base'], auth_url['authenticate'])
        self.__authorize_url = urllib.parse.urljoin(auth_url['base'], auth_url['authorize'])
        self.__authorization_result = None
        self.__app_uri = f'https://{self.__host}:{self.__port}'

    def get_access_token(self):
        params = {
            'client_id': self.__client_credential['id'],
            'grant_type': 'authorization_code',
            'redirect_uri': self.__app_uri,
            'response_type': 'code',
            'state': self.__randomname(40)
        }
        access_url = '?'.join([self.__authenticate_url, urllib.parse.urlencode(params)])

        # 認可コードリクエスト
        self.__authenticate(access_url)

        # トークンリクエスト
        handler = lambda request, address, server: AccessTokenRequestHandler(
            request, address, server,
            self.__client_credential, self.__app_uri,
            self.__authorize_url
        )
        with HTTPServer((self.host, self.port), handler) as server:
            print(f'Server Starts - {self.host}:{self.port}')
            server.socket = self.__wrap_socket_ssl(server.socket)

            try:
                while self.__authorization_result is None:
                    server.result = None
                    server.handle_request()
                    self.__authorization_result = server.result
            except KeyboardInterrupt:
                pass

        print(f'Server Stops - {self.host}:{self.port}')

    @property
    def result(self):
        return self.__authorization_result

    @property
    def host(self):
        return self.__host

    @property
    def port(self):
        return self.__port

    def __authenticate(self, access_url):
        open_new(access_url)

    def __wrap_socket_ssl(self, socket):
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain('./ssl_test.crt', keyfile='./ssl_test.key')
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        return context.wrap_socket(socket)

    def __randomname(self, n):
        randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
        return ''.join(randlst)
