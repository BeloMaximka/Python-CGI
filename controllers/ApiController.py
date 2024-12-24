import json
from models.RestModel import *
import urllib
import urllib.parse

class ApiController:
    def __init__(self):
        self.response = RestModel()


    def end_with(self, status_code:int=200, data:any=None):
        if status_code != 200:
            self.response.status = RestStatus(status_code)
            print("Status: %d %s" % (status_code, self.response.status.reasonPhrase))
            print("Access-Control-Allow-Origin: *")
            print("Content-Type: text/plain; charset=utf-8")
            print()
            print(self.response.status.reasonPhrase)
            exit()
        if data != None:
            self.response.data = data
            print("Access-Control-Allow-Origin: *")
            print("Content-Type: application/json; charset=utf-8")
            print()
            print(json.dumps(self.response.to_dict(), indent=2, default=vars))
            exit()


    def serve(self, am_data):
        method = am_data["envs"]["REQUEST_METHOD"]

        query_string = urllib.parse.unquote(am_data["envs"]["QUERY_STRING"], encoding="utf-8")
        query_params = dict(urllib.parse.parse_qsl(query_string))
        self.db_context = am_data["db_context"]
        self.am_data = am_data
        self.response.meta = RestMeta({
            "service": "Server Application",
            "group": "KN-P-213",
            "method": method,
            "params": query_params
        })
        action_name = f"do_{method.lower()}"
        controller_action = getattr(self, action_name, None)
        if controller_action != None:
            self.end_with(data=controller_action())
        else :
            self.end_with(405, "Method Not Allowed")