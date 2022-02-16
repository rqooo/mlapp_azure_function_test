import urllib.request
import json
import os

def predict_rent(pred_dict):
    data = {
        "Inputs": {
            "data":pred_dict
        }
    }
    body = str.encode(json.dumps(data))

    url = 'https://endpoint-20220204.japaneast.inference.ml.azure.com/score'
    api_key = '42WVU6ORNfdN5EaakOouOeoos3GgfU2A'
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        pred_result = json.loads(response.read())
        
    except urllib.error.HTTPError as error:
        error_msg = {'Results':"The request failed"}
        pred_result = json.loads(error_msg)
        
    return pred_result