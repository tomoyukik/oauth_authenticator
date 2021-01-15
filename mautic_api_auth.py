# %%
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import urlopen, HTTPError
from webbrowser import open_new
import requests
import json
import random, string
import urllib.parse
import urllib.request

# %%
MAUTIC_API_BASE_URL = 'http://0.0.0.0'

class HTTPServerHandler(BaseHTTPRequestHandler):
  def __init__(self, request, address, server, client_id, client_secret):
    print('server hander called')
    self._client_id = client_id
    self._client_secret = client_secret
    print('リクエスト')
    print(request)
    print('アドレス')
    print(address)
    print('サーバ')
    super().__init__(request, address, server)


  def do_GET(self):
    print('get received')
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()

    # リダイレクトURLからコードが取得できたらアクセストークンを取得する
    if 'code' in self.path:
      print('path:', self.path)
      params = self.path.split('&')
      print(params)
      state = params[0].replace('/?state=', '')
      print('state:', state)
      code = params[1].replace('code=', '')
      print('code:', code)
      url = f'{MAUTIC_API_BASE_URL}/oauth/v2/token'
      headers = {'Content-Type': 'application/json'}
      params = {
        'client_id': self._client_id,
        'client_secret': self._client_secret,
        'grant_type': 'authorization_code',
        'redirect_uri': 'http://0.0.0.0:8888', #urllib.parse.quote('http://0.0.0.0:8888', safe=''),
        'code': code
      }
      print('"client_id":', self._client_id)
      print('"client_secret":', self._client_secret)
      print('"redirect_uri":', urllib.parse.quote('http://0.0.0.0:8888', safe=''))
      print('"code":', code)
      print('post request', '&'.join(['='.join(p) for p in params.items()]))
      # response = requests.request(
      #   method='POST',
      #   url=url,
      #   # headers=headers,
      #   data=json.dumps(params)
      # )
      response = requests.post(url, data=params)
      self.wfile.write(bytes('<html><h1>Please close the window.</h1></html>', 'utf-8'))
      self.server.access_token = None
      print(response.status_code)
      print(response.content)
      if response.status_code == 200:
        print(response.json)
        self.server.access_token = response.json()['access_token']

class MauticAccessTokenHandler:
  def __init__(self, client_id, client_secret):
    print('token hander called')
    self._client_id = client_id
    self._client_secret = client_secret

  def get_access_token(self):
    params = {
      'client_id': self._client_id,
      'grant_type': 'authorization_code',
      'redirect_uri': urllib.parse.quote('http://0.0.0.0:8888', safe=''),
      'response_type': 'code',
      'state': self._randomname(40)
    }
    access_url = self._join_url(MAUTIC_API_BASE_URL, '/oauth/v2/authorize', params)
    print(f'get request to {access_url}')
    open_new(access_url)
    print('start server')
    httpServer = HTTPServer(
      ('0.0.0.0', 8888),
      lambda request, address, server: HTTPServerHandler(
        request, address, server, self._client_id, self._client_secret
      )
    )
    httpServer.handle_request()
    return httpServer.access_token


  def _randomname(self, n):
    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    return ''.join(randlst)

  def _join_url(self, base_url, sub_directory, params):
    params_joined = '&'.join(['='.join(p) for p in params.items()])
    joined_url = ''.join([base_url, sub_directory])
    return '?'.join([joined_url, params_joined])

