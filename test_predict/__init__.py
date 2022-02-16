import logging
import json
import azure.functions as func
from .response import create_response


def main(req: func.HttpRequest) -> func.HttpResponse:

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("There seems to be an error in the request body")
    else:
        res_body = create_response(req_body)

    return func.HttpResponse(res_body,mimetype="application/json")