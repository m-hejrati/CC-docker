from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json
import requests
from requests.api import request
import yaml
import os
import socket


HOST = "0.0.0.0"
PORT = 8080
ADDRESS = "http://worldtimeapi.org/api/timezone/asia/tehran"


def load_config():
    if os.path.exists("config.yml"):
        print("Load config file")
        with open("config.yml", 'r') as f:
            config_file = yaml.safe_load(f)
            PORT = config_file["address"]
            ADDRESS = config_file["port"]
    else:
        print("Use default address and port")


def get_time():
    time = requests.get(ADDRESS)
    return time.text


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        time = get_time()

        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps({
            'hostname': socket.gethostname(),
            'time': time,
        }).encode())
        return


if __name__ == '__main__':

    load_config()

    server = HTTPServer((HOST, PORT), RequestHandler)

    print(socket.gethostbyname(socket.gethostname()), ":", PORT)
    print('Starting server at ', HOST, ':', PORT)
    server.serve_forever()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    print("Server stop")

# fork from "http json echo server written in python3"
# https://gist.github.com/bsingr/a5ef6834524e82270154a9a72950c842#file-http-json-echo-py
