import requests
import json


auth = {
    'username': 'admin_json',
    'password': 'GRb%@vd23sb2'
}

url = 'https://88.204.147.90/AmanatCentral/hs/AmanatHTTP/GetAgentList'

resp = requests.get(url, auth=(auth['username'], auth['password']), verify=False)

print(json.dumps(resp.json(), indent=4))
