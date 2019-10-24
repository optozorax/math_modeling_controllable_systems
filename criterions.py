from texttable import Texttable
from math import ceil
import numpy as np

import matplotlib.pyplot as plt

def pretty_print(matrix):
	t = Texttable(100000)
	t.add_rows(matrix)
	print(t.draw())


def allocate_matrix(value, width, height):
	return [[value for x in range(width)] for y in range(height)]


class RausCriterion:
	def __init__(self, data):
		# Откуда берутся эти размеры?
		# Я правильно написал?
		self.width = int(len(data) / 2 + len(data) % 2)
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

			print("Delta " + str(i) + ":")
			print(minor)
			print("Determinant: ", self.determinants[-1])

	def check_criterion(self):
		for i in self.determinants:
			if i <= 0:
				return False
		return True


class Hodograph:
	def __init__(self, data):
		self.k_X = []
		self.k_Y = []
		self.data = data

	def replace_s_with_iw(self):
		n = len(self.data)
		for i in range(n - 3, -1, -4):
			self.data[i] = -self.data[i]
		for i in range(n - 4, -1, -4):
			self.data[i] = -self.data[i]

		for i in range(n - 1, -1, -2):
			self.k_X.append(self.data[i])
			self.k_X.append(0)
		for i in range(n - 2, -1, -2):
			self.k_Y.append(0)
			self.k_Y.append(self.data[i])

		self.k_X.reverse()
		self.k_Y.reverse()

	def print_X_and_Y(self):
		# Небольшие костыли с terms[3:] и terms[1] == '-'
		print("Проведём замену D(s) = D(iw) и получим:")
		print("X(w) = ", end="")
		terms = ""
		n = len(self.k_X)
		for i in range(n):
			if self.k_X[i] > 0:
				terms += " + {}*w^{}".format(self.k_X[i], n - i - 1)
			elif self.k_X[i] < 0:
				terms += " - {}*w^{}".format(abs(self.k_X[i]),n - i - 1)
		if terms[1] == "-":
			print(terms, " = 0")
		else:
			print(terms[3:], " = 0")

		print("Y(w) = ", end="")
		terms = ""
		n = len(self.k_Y)
		for i in range(n):
			if self.k_Y[i] > 0:
				terms += " + {}*w^{}".format(self.k_Y[i], n - i - 1)
			elif self.k_Y[i] < 0:
				terms += " - {}*w^{}".format(abs(self.k_Y[i]), n - i - 1)
		if terms[1] == "-":
			print(terms, " = 0")
		else:
			print(terms[3:], " = 0")

	def calc_w_roots(self):
		self.w_X_roots = list(set(np.roots(self.k_X).round(decimals=3)))
		self.w_Y_roots = list(set(np.roots(self.k_Y).round(decimals=3)))
		self.w_X_roots = list(filter(lambda a: a.real >= 0 and a.imag == 0, self.w_X_roots))
		self.w_Y_roots = list(filter(lambda a: a.real >= 0 and a.imag == 0, self.w_Y_roots))
		self.w_X_roots = np.real(self.w_X_roots)
		self.w_Y_roots = np.real(self.w_Y_roots)
		print("Найдём корни w:")
		print("по X = 0: ", self.w_X_roots)
		print("по Y = 0: ", self.w_Y_roots)

	def calc_X(self, w):
		x = 0.0
		n = len(self.k_X)
		for i in range(n):
			x += self.k_X[i]*w**(n - i - 1)
		return x

	def calc_Y(self, w):
		y = 0.0
		n = len(self.k_Y)
		for i in range(n):
			y += self.k_Y[i]*w**(n - i - 1)
		return y

	def build_table(self):
		self.table = []
		for w in self.w_X_roots:
			self.table.append([w, self.calc_X(w), self.calc_Y(w)])
		for w in self.w_Y_roots:
			self.table.append([w, self.calc_X(w), self.calc_Y(w)])
		self.table = sorted(self.table, key=lambda x: x[0])

	def print_table(self):
		newtable = [['w'] + ['X(w)'] + ['Y(w)']]
		for row in self.table:
			newtable.append(row)
		print('Таблица для построения годографа: ')
		pretty_print(newtable)

	def draw_hodograph(self):
		fig, axes = plt.subplots()
		x = [row[1] for row in self.table]
		y = [row[2] for row in self.table]
		x_new = []
		y_new = []
		x_ticks = []
		y_ticks = []
		new_points = 4
		for elem in x:
			x_ticks += elem
			x_ticks -= elem
		for elem in y:
			y_ticks += elem
			y_ticks -= elem

		new_points_count = 4
		for i in range(len(x) - 1):
			if x[i] != x[i+1]:
				x_new += (np.arange(x[i], x[i+1], (x[i+1]-x[i]) / new_points_count).tolist())
			else:
				x_new += [0.0 for x in range(new_points_count)]
			if y[i] != y[i+1]:
				y_new += (np.arange(y[i], y[i+1], (y[i+1]-y[i]) / new_points_count).tolist())
			else:
				y_new += [0.0 for y in range(new_points_count)]
		x_new.append( x[len(x) - 1] )
		y_new.append( y[len(y) - 1] )

		plt.plot(x_new, y_new)
		for i in range(len(x)):
			plt.scatter(x[i], y[i], c='black')

		plt.xlabel('X', fontsize=10)
		plt.ylabel('Y', fontsize=10)
		plt.xscale('symlog', linthreshy=0.2)
		plt.yscale('symlog', linthreshy=0.2)
		plt.xticks(x_ticks)
		plt.yticks(y_ticks)
		plt.axhline(0, color='grey')
		plt.axvline(0, color='grey')
		plt.tick_params(axis='both', labelsize=8)
		plt.grid(alpha=0.4)
		return plt


	def check_criterion(self):
		for i in range(0, len(self.table), 4): # ox +
			if self.table[i][1] <= 0 or abs(self.table[i][2]) > 0.01:
				return False
		for i in range(1, len(self.table), 4): # oy -
			if self.table[i][2] <= 0 or abs(self.table[i][1]) > 0.01:
				return False
		for i in range(2, len(self.table), 4): # ox -
			if self.table[i][1] >= 0 or abs(self.table[i][2]) > 0.01:
				return False
		for i in range(3, len(self.table), 4): # oy -
			if self.table[i][2] >= 0 or abs(self.table[i][1]) > 0.01:
				return False

		return True



def print_result(data):
	np.set_printoptions(linewidth=100000)

	print("Вычисление по алгебраическому критерию: ")
	table = RausCriterion(data)
	table.calc_table()
	table.print()
	if (table.check_criterion):
		print("Это устойчивая схема.")
	else:
		print("Это неустойчивая схема.")

	print("")

	print("Вычисление по критерию Гурвица: ")
	matrix = HurwitsCriterion(data)
	matrix.calc_determinants()
	if (matrix.check_criterion):
		print("Это устойчивая схема.")
	else:
		print("Это неустойчивая схема.")

	print("")

	print("Вычисление по критерию Михайлова: ")
	print("Внимание! Критерий может отобраться неправильно")
	print("Критерий устойчивости:")
	print("- начинается на положительной полуоси абсцисс")
	print("- вращение против часовой стрелки вокруг начала координат")
	print("- проходит {} квадрантов".format(len(data) - 1))
	table = Hodograph(data)
	table.replace_s_with_iw()
	table.print_X_and_Y()
	table.calc_w_roots()
	table.build_table()
	table.print_table()
	if (table.check_criterion):
		print("Это устойчивая схема.")
	else:
		print("Это неустойчивая схема.")
