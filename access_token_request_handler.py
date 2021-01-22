from http.server import BaseHTTPRequestHandler
import urllib.parse
import requests

class AccessTokenRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, address, server, client_credential, client_url, authorize_url):
        self.__client_credential = client_credential
        self.__authorize_url = authorize_url
        self.__client_url = client_url
        super().__init__(request, address, server)

    def do_GET(self):
        self.__responde_200()

        # アクセストークン取得
        if 'code' in self.path:
            response = self.__request_access_token()
            self.server.result = response
            self.__write_response_message(response)
            return

        self.wfile.write(bytes('failed to get authorization code.', 'utf-8'))
        return

    def __write_response_message(self, response):
        print('status code:', response.status_code)
        self.__wfwrite(f'Status Code: {response.status_code}')
        print('response:', response.reason)
        self.__wfwrite(f'Response: {response.reason}')
        print(response.json())
        if response.ok:
            self.__wfwrite('<br>'.join([f'{k}: {v}' for (k, v) in response.json().items()]))
        else:
            self.__wfwrite(response.json()['errors'][0]['message'])

    def __wfwrite(self, string):
        self.wfile.write(bytes(f'<p>{string}</p>', 'utf-8'))

    def __responde_200(self):
        self.send_response(200)
        self.end_headers()

    def __request_access_token(self):
        params = self.__params_from_path()

        post_params = {
            'client_id': self.__client_credential['id'],
            'client_secret': self.__client_credential['secret'],
            'grant_type': 'authorization_code',
            'redirect_uri': self.__client_url,
            'code': params['code']
        }
        response = requests.post(self.__authorize_url, data=post_params, verify=False) # WARN: verify=False
        return response

    def __params_from_path(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        return params
