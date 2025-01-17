import requests
import json

url = 'http://gateway.amanat.systems'

'''
1 - FunSun
2 - Kompas
3 - JoinUp
'''

partners = {
    1: {
        'username': 'info@fstravel.kz',
        'password': '8mj1NoBGWt'
    },
    2: {
        'username': 'hr@kompastour.kz',
        'password': 'Uk@bEM'
    },
    3: {
        'username': 'a.yakupova@joinup.kz',
        'password': 'PwaY$E'
    }
}


def get_auth_token(partner, url=url):
    url += '/api/login'

    auth_data = {
        'login': partners[partner]['username'],
        'password': partners[partner]['password']
    }


    resp = requests.post(url, data=auth_data)
    return resp.json()['data']['access_token']


def set_cancellation(partner, policy_number, url=url):
    url += '/api/ost/set-cancellation-contract'
    headers = {'Authorization': 'Bearer ' + get_auth_token(partner)}

    resp = requests.post(url, headers=headers, params={'policy_number': policy_number})

    # return f"------------------------------------------------------------\n{resp.json().get('success')}\n{resp.json().get('message')}\n------------------------------------------------------------"
    return resp.json()


def set_policy(partner, url=url):
    with open('bodyOST', encoding='utf-8') as f:
        body = json.load(f)

    body["from"] = "Support"

    url += '/api/ost/set-policy'
    headers = {'Authorization': 'Bearer ' + get_auth_token(partner)}

    resp = requests.post(url, headers=headers, json=body)
    return f"-------------------------------------------РЕЗУЛЬТАТ-------------------------------------------\n{resp.json()['success']}\n{resp.json()['message']}\n{resp.json()['errors']}\n-----------------------------------------------------------------------------------------------"
