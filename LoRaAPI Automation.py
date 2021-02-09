import urllib.request, json
from urllib.request import Request, urlopen
import urllib
import requests
from requests.auth import HTTPDigestAuth
from requests.auth import HTTPBasicAuth
import json

#req = Request('https://www.postman.com/collections/4ebd5e8ec105c9c245d6/', headers={'User-Agent': 'Mozilla/5.0'})
#webpage = urlopen(req).read()
#print (webpage)

parametersLora = {
    "format":"json",
    "limit":"1"
   # "id": "6e34efc5-2585-461c-bd81-147c801a024c"
}

url = "https://ran.ap.everynet.io/api/v3.0/gateways?format=json"
headers = {"Content-Type": "application/json"}
auth = HTTPBasicAuth('EverynetTelkomNOC@gmail.com', '3veryn@t1')
#files = {'filename': open('filename','rb')}

req = requests.get(url, headers=headers , auth=auth)# , files=files)

LoRa = requests.get(url,headers=headers, auth=auth, params=parametersLora)
print("LoRa status code", LoRa.status_code)

#print(PGN.json())
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)
    
#jprint(PGN.json())
#jprint(req.json())
jprint(LoRa.json())
