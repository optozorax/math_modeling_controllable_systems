#!/usr/bin/python3 -u
# Примечание: эта опция '-u' обязательна, если вы хотите смотреть логи в systemctl status

# Эта программа реализует решение критериев через браузер
# Пример обращения: curl "localhost:80/calc_criterion/1,2,3,4,5"

# Локальные файлы
from criterions import *
from print_server import *


class Worker(PrintServer):
    def work(self):
        prefix = '/calc_criterion/'
        if self.path.startswith(prefix):
            array = self.path[len(prefix):].split(',')
            data = [float(i) for i in array]
            print_result(data)
        else:
            print("Request has no '{}'".format(prefix))


def main():
	start_server(Worker)


if __name__ == "__main__":
	main()