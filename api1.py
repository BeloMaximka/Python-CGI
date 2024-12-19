#!python
import os
import urllib
import urllib.parse
import sys
import codecs
import json

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
sys.stdin = codecs.getreader("utf-8")(sys.stdin.detach())

def is_http_header(k: str):
    return k.startswith("HTTP_") or k in ('CONTENT_TYPE, CONTENT_LENGTH')

def format_header_name(k: str):
    return (k[5:] if k.startswith('HTTP_') else k).lower().replace('_', '-')

def get_http_headers(items):
    return {format_header_name(k): v for k,v in items if is_http_header(k)}

def send_error(code: int=400, phrase:str ="Bad Request"):
    print("Status: %d %s" % (code, phrase))
    print("Content-Type: text/plain; charset=utf-8")
    print()
    print(phrase)




def handle():
    envsUI = "<ul>" + ''.join("<li>%s = %s</li>" % (k,v) for k,v in os.environ.items()) + "</ul>"
    envs = {k: v for k,v in os.environ.items()}
    query_string = urllib.parse.unquote(envs["QUERY_STRING"], encoding="utf-8")
    query_params = dict(urllib.parse.parse_qsl(query_string))

    headers = get_http_headers(os.environ.items())
    body_parameters = {}
    body = sys.stdin.read()
    if body != '':
        if headers['content-type'] == 'application/json':
            body_parameters = json.loads(body)
        elif headers['content-type'] == 'application/x-www-form-urlencoded':
            body_parameters = dict(urllib.parse.parse_qsl(urllib.parse.unquote(body)))
        else:
            send_error(415, "Unsupported Media Type. Supported MIME: 'application/json', 'application/x-www-form-urlencoded'")
            return

    path = envs['REQUEST_URI']
    if '?' in path:
        path = path[:(path.index('?'))]

    print("Content-Type: text/plain; charset=utf-8")
    print()
    print(f"<b>Method</b>: {envs["REQUEST_METHOD"]}", end='<br>')
    print()
    print(f"<b>Headers</b>: {headers}", end='<br>')
    print()
    print(f"<b>Query params</b>: {query_params}" , end='<br>')
    print()
    print(f"<b>Body</b>: {body_parameters}", end='<br>')

handle()