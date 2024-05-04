# import ssl
# import http.server
# httpd = http.server.HTTPServer(('localhost', 443), http.server.SimpleHTTPRequestHandler)
# httpd.socket = ssl.wrap_socket(httpd.socket, certfile='./certificate.pem', server_side=True, ssl_version=ssl.PROTOCOL_TLS)
# httpd.serve_forever()

import json

import clickhouse_connect
from clickhouse_driver import Client
env_file = "seminar3/clickhouse.json"
with open(env_file) as f:
    data = json.load(f)
    username = data.get("username")
    password = data.get("password")

# client = clickhouse_connect.get_client(
    # host='cmttji3td8.europe-west4.gcp.clickhouse.cloud',
client = Client(
    host='127.0.0.1',
    port=8123,
    user=username,
    password=password,
    secure=True)
print("Result:", client.execute("SHOW DATABASES"))

