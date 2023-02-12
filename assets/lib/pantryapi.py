# Pantryapi: Library to work with pantryapi
# Version 1.0, Made by: Simon Kalmi Claesson
#

import requests

# Web request handler for the pantry http api
def pantryapi(_id, method, body=None, basket=None):
    method = method.lower()
    url = f"https://getpantry.cloud/apiv1/pantry/{_id}"
    if basket:
        url += f"/basket/{basket}"
    headers = {'Content-Type': 'application/json'}
    
    if method == 'get':
        response = requests.get(url, headers=headers)
    elif method == 'put':
        response = requests.put(url, headers=headers, json=body)
    elif method == 'post':
        response = requests.post(url, headers=headers, json=body)
    else:
        raise ValueError(f"Invalid method '{method}'")

    return response


# Abstraction layer for better understanding and easier access to the pantry api
def pantryapireq(key, basket=None, json=None, mode=None):
    if mode != None: mode = mode.lower()
    if mode == 'getall':
        ans = pantryapi(key, "GET")
    elif mode == 'get':
        ans = pantryapi(key, "GET", basket=basket)
    elif mode == 'append':
        ans = pantryapi(key, "PUT", basket=basket, body=json)
    elif mode in ['create', 'replace']:
        if json:
            ans = pantryapi(key, "POST", basket=basket, body=json)
        else:
            ans = pantryapi(key, "POST", basket=basket)
    else:
        raise ValueError("Invalid mode")
    return ans
