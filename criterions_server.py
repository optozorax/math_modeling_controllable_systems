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


prefix_criterion     = '/calc_criterion/'
prefix_criterion_png = '/calc_criterion_png/'
prefix_diffur        = '/calc_diffur/'


def criterion_parse_path(path):
    array = path.split(",")
    return [float(i) for i in array]


def work_criterion(path):
    print("<pre>");
    data = criterion_parse_path(path)
    print_result(data)
    print('</pre><img src="/calc_criterion_png/{path}" style="max-width: 100%; width: 500px;">'.format(path=path))


def work_criterion_png(path):
    data = criterion_parse_path(path)

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

    return (result, "image/png")


def work_diffur(path):
    calc_diffur(path)


class Worker(PrintServer):
    def cut_prefix(self):
        path = self.path
        path = path[1:]
        path = path[path.find('/')+1:]
        return path

    def work(self):
        if self.path.startswith(prefix_criterion_png):
            return work_criterion_png(self.cut_prefix())
        elif self.path.startswith(prefix_criterion):
            return work_criterion(self.cut_prefix())
        elif self.path.startswith(prefix_diffur):
            return work_diffur(self.cut_prefix())
        else:
            raise Exception("404: calculator '{}' not found".format(self.path))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=81, type=int)
    return parser.parse_args()


def main():
    args = parse_args()
    start_server(Worker, args.port)


if __name__ == "__main__":
    main()
