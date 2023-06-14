from client import Client

class Request(object):
    
    def __init__(self):
        self.client = Client()
        # Issue a series of API requests an example. For use this test, you must first subscribe to the arome api with your application
        self.client.session.headers.update({'Accept': 'application/json'})
    
    def obtainData(self, endpoint_url, method):
        return self.client.request(method, endpoint_url, verify=False)
    
