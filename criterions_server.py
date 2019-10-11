#!/usr/bin/python3 -u

# Примечание: эта опция '-u' обязательна, если вы хотите смотреть логи в systemctl status

# Эта программа реализует решение критериев через браузер
# Пример обращения: curl "localhost:80/calc_criterion/1,2,3,4,5"

# Локальные файлы
from criterions import *
from print_server import *

import argparse
import os


class Worker(PrintServer):
    prefix = '/calc_criterion/'

    def parse_path(self, path):
        array = path[len(self.prefix):].split(',')
        data = [float(i) for i in array]        
        return data

    def work_text(self):
        if self.path == "/index.html":
            a = os.path.realpath(__file__)
            a = a[:a.rfind('/')]
            print(open(a + '/index.html').read())
        elif self.path.startswith(self.prefix):
            print("<pre>");
            data = self.parse_path(self.path)            
            print_result(data)
            print('</pre><img src="{path}.png">'.format(path=self.path))
        else:
            raise Exception("Request has no '{}'".format(self.prefix))
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
