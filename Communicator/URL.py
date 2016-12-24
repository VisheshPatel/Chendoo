'''
Created on Dec 24, 2016
@author: Vishal Chovatiya
'''
import requests


class URLprocessor:
    " Do All Things Related To Communicating "
    url = None
    headers = {'user-agent': 'my-app/0.0.1'}
    status_code = None
    response = None
    encoding = None
    content = None
    json = None

    def __init__(self, url):
        " Request On Object Creations "
        self.requester(url)

    def requester(self, url):
        " Requesting URL "
        try:
            res = requests.get(url, headers=None)
        except requests.ConnectionError:
            print "Error: Check For Internet Connection"
        except requests.Timeout:
            print "Error: Request Time-Out"
        else:
            if res.status_code == 200:
                self.url = res.url
                self.response = res.text
                self.status_code = res.status_code  # TODO: Error Handling

                # Now Not In Use
                #self.headers = res.headers
                #self.encoding = res.encoding
                #self.content = res.content
                # res.raise_for_status()
                #self.json = res.json()
            else:
                print "Error: HTTPError ", res.status_code

    def refresher(self):
        " Just A Wrapper To Request Again"
        self.requester(self.url)
