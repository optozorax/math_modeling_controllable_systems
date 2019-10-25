#!/usr/bin/python3 -u

# Примечание: эта опция '-u' обязательна, если вы хотите смотреть логи в systemctl status

# Эта программа реализует решение критериев через браузер
# Пример обращения: curl "localhost:80/calc_criterion/1,2,3,4,5"

# Локальные файлы
from criterions import *
from print_server import *
from diffur import *

import argparse
import os


class Worker(PrintServer):
    prefix = '/calc_criterion/'
    prefix_diffur = '/calc_diffur/'

    def parse_path(self, path):
        array = path[len(self.prefix):].split(',')
        data = [float(i) for i in array]
        return data

    def print_file(self, filename):
        a = os.path.realpath(__file__)
        a = a[:a.rfind('/')]
        print(open(a + '/' + filename).read())

    def work(self):
        if self.path == "/index.html" or self.path == "/":
            self.print_file("index.html")
        elif self.path =="/algebraiccriterions.html":
            self.print_file("algebraiccriterions.html")
        elif self.path == "/diffur.html":
            self.print_file("diffur.html")
        elif self.path == "/main.js":
            self.print_file("main.js")
            self.content_type = 'application/javascript'
        elif self.path == "/style.css":
            self.print_file("style.css")
            self.content_type = 'text/css'
        elif self.path.endswith(".png"):
            return self.work_png()
        elif self.path.startswith(self.prefix):
            print("<pre>");
            data = self.parse_path(self.path)
            print_result(data)
            print('</pre><img src="{path}.png" style="max-width: 100%; width: 500px;">'.format(path=self.path))
        elif self.path.startswith(self.prefix_diffur):
            calc_diffur(self.path[len(self.prefix_diffur):])
        else:
            raise Exception("404: resource '{}' not found".format(self.path, self.prefix))

    def work_png(self):
        if self.path.startswith(self.prefix):
            data = self.parse_path(self.path[:-4])

            h = Hodograph(data)
            h.replace_s_with_iw()
            h.calc_w_roots()
            h.build_table()
            graph = h.draw_hodograph()

            buf = io.BytesIO()
            graph.savefig(buf, format='png')
            buf.seek(0)
            result = buf.getvalue()
            buf.close()

            self.content_type = "image/png"

            return result
        else:
            raise Exception("Request has no '{}'".format(self.prefix))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=80, type=int)
    return parser.parse_args()


def main():
    args = parse_args()
    start_server(Worker, args.port)


if __name__ == "__main__":
    main()

