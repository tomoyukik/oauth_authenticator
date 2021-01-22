from oauth_authenticator import OAuthAuthenticator
import yaml

AUTH_BASE_URL = 'https://0.0.0.0/oauth/v2/'
AUTHENTICATE_PATH = 'authorize'
AUTHORIZE_PATH = 'token'
APP_HOST = '0.0.0.0'
APP_PORT = 8888

if __name__ == '__main__':
    with open('./credential.yaml') as file:
        credential = yaml.safe_load(file)
    authenticator = OAuthAuthenticator(
        {'id': credential['id'], 'secret': credential['secret']},
        {'host': APP_HOST, 'port': APP_PORT},
        {'base': AUTH_BASE_URL, 'authenticate': AUTHENTICATE_PATH, 'authorize': AUTHORIZE_PATH}
    )
    authenticator.get_access_token()
    print('結果', authenticator.result.json())
