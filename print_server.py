# Библиотека, которая хостит в качестве сервера python-скрипт, при этом выводит в браузер всё, что выводит этот скрипт. Аналогично выводятся в браузер все исключения

import http.server
import socketserver
from http import HTTPStatus
import io
import traceback
from contextlib import redirect_stdout


class PrintServer(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(HTTPStatus.OK)
        self.send_header('content-type','text/html; charset=utf-8')
        self.end_headers()
        with io.StringIO() as buf, redirect_stdout(buf):
            print("<pre>")
            try:
                self.work()
            except Exception as e:
                print(traceback.format_exc())
            print("</pre>")
            self.wfile.write(buf.getvalue().encode('utf-8'))

    def work(self):
        print("Not realized method 'work'")


def start_server(worker_type, port=80):
    httpd = socketserver.TCPServer(('', port), worker_type)
    httpd.serve_forever()
