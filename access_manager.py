#!python

import sys
import codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
sys.stdin = codecs.getreader("utf-8")(sys.stdin.detach())

import os
import json

def send_error(code: int=400, phrase:str ="Bad Request", explain: str=None):
    print("Content-Type: text/plain; charset=utf-8")
    print("Status: %d %s" % (code, phrase))
    print()
    print(explain if explain != None else phrase, end="")
    exit()


def send_file(filename:str):
    print("Content-Type: text/html; charset=utf-8")
    print()
    with open(filename, encoding="utf-8") as file:
        print(file.read())
    exit()

def send_json(body:str):
    print("Content-Type: application/json; charset=utf-8")
    print()
    print(json.dumps(body))
    exit()


envs = {k: v for k,v in os.environ.items()}
path = envs['REQUEST_URI']

if path.startswith("/"):
    path = path[1:]

if "?" in path:
    path = path[:(path.index("?"))]

if path == "":
    send_file("home.html")
else:
    parts = path.split("/", maxsplit=2)
    controller = parts[0]
    action = parts[1] if len(parts) > 1 else "base"
    slug = parts[2] if len(parts) > 2 else None
    controller_name =  f"{parts[0].title()}{action.title()}Controller"

    sys.path.append('./')
    import importlib
    
    try:
        controller_module = importlib.import_module(f"controllers.{controller}.{controller_name}")
        controller_class = getattr(controller_module, controller_name)
        controller_object = controller_class()
        action_name = f"do_{envs["REQUEST_METHOD"].lower()}"
        controller_action = getattr(controller_object, "serve")
        controller_action({
            'envs': envs,
            'path': path,
            'controller': controller,
            "category": action,
            "slug": slug
        })
    except Exception as err:
        send_error(explain=err)

    print("Content-Type: text/html; charset=utf-8")
    print()
    print("Controller: %s, Action: %s, Slug: %s, Class: %s" % (controller, action, slug, controller_name))
    exit()

send_file("index.html")
    