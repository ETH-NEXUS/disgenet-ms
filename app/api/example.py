"""
Script example to use the DisGeNET REST API with the new authentication system
"""

import requests

api_host = "https://www.disgenet.org/api"
api_key = "bcb8227e319abb606eb3a56c2167120950abfa7e"
s = requests.Session()

if api_key:
    s.headers.update({"Authorization": "Bearer %s" % api_key})
    gda_response = s.get(api_host + '/vda/variant/rs295')
    print(gda_response.json())

if s:
    s.close()

