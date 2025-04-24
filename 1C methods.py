import requests
import json
import os


auth = {
    'username': os.getenv('LOGIN_1C'),
    'password': os.getenv('PASSWORD_1C')
}

url = os.getenv('GET_AGENT_LIST')

resp = requests.get(url, auth=(auth['username'], auth['password']), verify=False)

print(json.dumps(resp.json(), indent=4))
