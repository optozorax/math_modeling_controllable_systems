#!/usr/bin/python3

# Эта программа реализует решение критериев через консоль
# Пример использования: 1 2 3 4 5

from criterions import *


def main():
	x = input("Введите коэффициенты многочлена B(s):\n")
	data = [int(i) for i in x.split()]

	print_result(data)


if __name__ == "__main__":
	main()
