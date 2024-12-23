import json
from models.RestModel import *

class ApiController:
    def __init__(self):
        self.response = RestModel()


    def end_with(self, status_code:int=200, data:any=None):
        if status_code != 200:
            self.response.status = RestStatus(status_code)
            print("Status: %d %s" % (status_code, self.response.status.reasonPhrase))
            print("Content-Type: text/plain; charset=utf-8")
            print()
            print(self.response.status.reasonPhrase)
            exit()
        if data != None:
            self.response.data = data
            print("Content-Type: application/json; charset=utf-8")
            print()
            print(json.dumps(self.response.to_dict(), indent=2))
            exit()


    def serve(self, am_data):
        method = am_data["envs"]["REQUEST_METHOD"]
        self.am_data = am_data
        self.response.meta = RestMeta({
            "service": "Server Application",
            "group": "KN-P-213",
            "method": method
        })
        action_name = f"do_{method.lower()}"
        controller_action = getattr(self, action_name, None)
        if controller_action != None:
            self.end_with(data=controller_action())
        else :
            self.end_with(405, "Method Not Allowed")