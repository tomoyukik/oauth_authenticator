from ssl_server_sample import OAuthAuthenticator

AUTHORIZATION_URL = 'https://0.0.0.0/oauth/v2/'
CLIENT_ID = '1_5j8ecbsu9cowo4wk8kwwcc8k8wc08c8o4sgo4s084cg880ggo0'
CLIENT_SECRET = '172h8p6mevy8w8cggc44gw4w4ookk4ockg440osggkw808c00g'
APP_URI = 'https://0.0.0.0:8888'
APP_HOST = '0.0.0.0'
APP_PORT = 8888

if __name__ == '__main__':
    client_info = (APP_HOST, APP_PORT)
    handler = OAuthAuthenticator(
        {'id': CLIENT_ID, 'secret': CLIENT_SECRET},
        AUTHORIZATION_URL,
        APP_URI
    )
    print('だから取れたぞー', handler.get_access_token())
