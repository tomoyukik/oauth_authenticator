# %%
import os
from mautic_api_auth import MauticAccessTokenHandler
# %%

def get_access_token(init=False):
    client_id = '1_5j8ecbsu9cowo4wk8kwwcc8k8wc08c8o4sgo4s084cg880ggo0'
    client_secret = '172h8p6mevy8w8cggc44gw4w4ookk4ockg440osggkw808c00g'

    # OAuth2認証でアクセストークンを取得する
    print('call token handler')
    token_handler = MauticAccessTokenHandler(client_id, client_secret)
    print('token_hander created')
    return token_handler.get_access_token()

# %%
if __name__ == '__main__':
    print('トークンとるよー')
    access_token = get_access_token()
    print(f'アクセストークンとれたよー: {access_token}')
# %%
