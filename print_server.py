# Библиотека, которая хостит в качестве сервера python-скрипт, при этом выводит в браузер всё, что выводит этот скрипт. Аналогично выводятся в браузер все исключения

import http.server
import socketserver
from http import HTTPStatus
import io
import traceback
from contextlib import redirect_stdout
import time


class PrintServer(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith(".png"):
            self.send_response(HTTPStatus.OK)
            
            buf = list()
            try:
                buf = self.work_png()
                self.send_header('content-type','image/png')
                self.send_header('content-length','{}'.format(len(buf)))
                self.end_headers()
            except Exception as e:
                buf = traceback.format_exc().encode('utf-8')

            self.wfile.write(buf)
        else:
            self.send_response(HTTPStatus.OK)
            self.send_header('content-type','text/html; charset=utf-8')
            self.end_headers()
            with io.StringIO() as buf, redirect_stdout(buf):
                try:
                    self.work_text()
                except Exception as e:
                    print("<pre>")
                    print(traceback.format_exc())
                    print("</pre>")
                self.wfile.write(buf.getvalue().encode('utf-8'))

    def work_text(self):
        print("Not realized method 'work_text'")

    def work_png(self):
        return "Not realized method 'work_png'".encode('utf-8')


def start_server(worker_type, port=80):
    for i in range(100):
        try:
            httpd = socketserver.TCPServer(('', port), worker_type)
            httpd.serve_forever()
        except OSError as e:
            if e.errno != 98:
                break
            print("Waiting a {} second for port {}".format(i, port))
            time.sleep(1)
        except Exception:
            server.shutdown()
            print("Sucessfully shutdown server")
            pass
