from texttable import Texttable
from math import ceil
import numpy as np


def pretty_print(matrix):
	t = Texttable()
	t.add_rows(matrix)
	print(t.draw())

def allocate_matrix(value, width, height):
	return [[value for x in range(width)] for y in range(height)]

class RausCriterion:
	def __init__(self, data):
		# Откуда берутся эти размеры?
		# Я правильно написал?
		self.width = ceil(len(data))
		self.height = len(data)
		self.guaranteed_not = False

		self.table = allocate_matrix(0.0, self.width, self.height)

		# По какому принципу это заполняется?
		# Я правильно написал?
		i = 0
		j = 0
		for elem in data:
			self.table[j][i] = float(elem)
			j += 1
			if j > 1:
				j = 0
				i += 1

	def __calc_d(self, i):
		return self.table[i-2][0]/self.table[i-1][0]

	def __calc_c(self, i, k):
		return self.table[i-2][k+1] - self.__calc_d(i) * self.table[i-1][k+1]

	def calc_table(self):
		try:
			for i in range(2, self.height):
				for j in range(0, self.width-1):
					self.table[i][j] = self.__calc_c(i, j)
		except:
			# Если произошло деление на 0
			self.guaranteed_not = True

	def print(self):
		newtable = [["i\\k"] + [i+1 for i in range(self.width)]]
		newtable += [[i+1] + self.table[i] for i in range(self.height)]
		pretty_print(newtable)

	def check_criterion(self):
		if self.guaranteed_not:
			return False
		for i in self.table:
			if i[0] <= 0:
				return False
		return True


class HurwitsCriterion:
	def __init__(self, data):
		self.n = len(data) - 1
		self.matrix = allocate_matrix(0, self.n, self.n)
		self.determinants = list()

		for i in range(self.n):
			for j in range(self.n):
				diag_no = j + 1
				diag_dist = j - i
				pos = diag_no + diag_dist
				if not(pos < 0 or pos >= len(data)):
					self.matrix[i][j] = data[pos]

	def calc_determinants(self):
		numpy_matrix = np.array(self.matrix)
		for i in range(1, self.n):
			minor = numpy_matrix[0:i, 0:i]
			self.determinants.append(np.linalg.det(minor))

			print(minor)
			print("Determinant: ", self.determinants[-1])

	def check_criterion(self):
		for i in self.determinants:
			if i <= 0:
				return False
		return True		


class LeinardChipathCriterion:
	def __init__(self, data):
		self.n = len(data) - 1
		self.matrix = allocate_matrix(0, self.n, self.n)
		self.determinants = list()

		for i in range(self.n):
			for j in range(self.n):
				diag_no = j + 1
				diag_dist = j - i
				pos = diag_no + diag_dist
				if not(pos < 0 or pos >= len(data)):
					self.matrix[i][j] = data[pos]

	def calc_determinants(self):
		numpy_matrix = np.array(self.matrix)
		for i in range(1, self.n, 2):
			minor = numpy_matrix[0:i, 0:i]
			self.determinants.append(np.linalg.det(minor))

			print(minor)
			print("Determinant: ", self.determinants[-1])

	def check_criterion(self):
		for i in self.determinants:
			if i <= 0:
				return False
		return True		


def main():
	#x = input("Введите коэффициенты многочлена B(s):\n")
	#data = [int(i) for i in x.split()]

	data = [1, 6, 15, 20, 15, 6, 1]
	#data = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
	print("Вычисление по алгебраическому критерию: ")
	table = RausCriterion(data)
	table.calc_table()
	table.print()
	print("Это устойчивая схема? {}".format(table.check_criterion()))

	print("")

	print("Вычисление по критерию Гурвица: ")
	matrix = HurwitsCriterion(data)
	matrix.calc_determinants()
	print("Это устойчивая схема? {}".format(matrix.check_criterion()))

	print("")

	print("Вычисление по критерию Льенара-Шипара: ")
	matrix = LeinardChipathCriterion(data)
	matrix.calc_determinants()
	print("Это устойчивая схема? {}".format(matrix.check_criterion()))

if __name__ == "__main__":
	main()
