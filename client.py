import config
import json
import requests
import time
import jwt
from datetime import date
from datetime import datetime
from datetime import timedelta



# Example of a Python implementation for a continuous authentication client.
# It's necessary to :
# - update APPLICATION_ID
# - update request_url at the end of the script

class Client(object):

    def __init__(self):
        self.session = requests.Session()

    def request(self, method, url, **kwargs):
        # First request will always need to obtain a token first
        if 'Authorization' not in self.session.headers:
            self.obtain_token()

        # Optimistically attempt to dispatch reqest
        response = self.session.request(method, url, **kwargs)
        if self.token_has_expired():
            # We got an 'Access token expired' response => refresh token
            self.obtain_token()
            # Re-dispatch the request that previously failed
            response = self.session.request(method, url, **kwargs)

        return response

    def token_has_expired(self):
        jwt_decode = jwt.decode(self.session.token,options={"verify_signature": False})
        now = datetime.now()
        second1 = now.timestamp()
        print('jwt : ', jwt_decode['exp'])
        print('now : ', second1)
        if second1 > jwt_decode['exp'] - 5:
            return True
        return False

    def obtain_token(self):
        # Obtain new token
        print('obtain token')
        data = {'grant_type': 'client_credentials'}
        headers = {'Authorization': 'Basic ' + APPLICATION_ID}
        access_token_response = requests.post(TOKEN_URL, data=data, verify=False, allow_redirects=False, headers=headers)
        # print(access_token_response)
        # print(access_token_response.json()['access_token'])
        token = access_token_response.json()['access_token']
        self.session.token = token
        # Update session with fresh token
        # print(token)
        self.session.headers.update({'Authorization': 'Bearer %s' % token})

# def main():
#     client = Client()
#     # Issue a series of API requests an example. For use this test, you must first subscribe to the arome api with your application
#     client.session.headers.update({'Accept': 'application/json'})
# 
#     for i in range(100):
#         response = client.request('GET', 'https://public-api.meteofrance.fr/public/DPVigilance/v1/textesvigilance/encours', verify=False)
#         print(response.json())
#         time.sleep(120)
# 
# 
# if __name__ == '__main__':
#     main()
