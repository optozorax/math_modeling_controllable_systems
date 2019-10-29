from sympy import *
from sympy.parsing.sympy_parser import parse_expr

# Парсит матрицу из списка, для которого: сначала введены ширина и высота, затем все элементы матрицы слева-направо и сверху-вниз
def read_matrix(array):
	w = int(array[0])
	h = int(array[1])
	result = [[0 for x in range(w)] for y in range(h)]
	counter = 2
	for i in range(h):
		for j in range(w):
			result[i][j] = parse_expr(array[counter])
			counter += 1
	array = array[counter:]
	return (array, Matrix(result))

# Класс для красивого вывода уравнения
class PrintEquation:
	def __enter__(self):
		print("\\(\\displaystyle ")

	def __exit__(self, type, value, traceback):
		print("\\)")
		print("<br>")

def calc_diffur(string):
	# Парсинг переданных данных
	array = string.split(",")
	array, A = read_matrix(array)
	array, G = read_matrix(array)
	array, X0 = read_matrix(array)
	array, C = read_matrix(array)

	t = symbols('t')
	tau = symbols('tau')

	# Символьные вычисления
	P, D = A.jordan_form()
	P1 = P**-1
	DE = exp(D)
	AED = P*DE*P1
	AE = exp(A)
	F = AE*exp(tau)

	FG = F*G
	FI = Matrix(FG)
	FI = FI.subs(tau, t - tau)
	for i in range(len(FI)):
		FI[i] = integrate(FI[i], (tau, 0, t))

	FX0 = F.subs(tau, t)*X0
	X = simplify(FX0 + FI)

	Y = simplify(C*X)

	# Вывод переданных данных
	with PrintEquation() as p:
		print("\\mathbf{A} = ", latex(A))
	with PrintEquation() as p:
		print("\\mathbf{X}(0) = ", latex(X0))
	with PrintEquation() as p:
		print("\\mathbf{G}(t) = ", latex(G))
	with PrintEquation() as p:
		print("\\mathbf{C} = ", latex(C))

	print("<br>")
	print("<br>")

	# Вывод формул, по которым производятся вычисления
	with PrintEquation() as p:
		print("\\mathbf{A} = P\\cdot D\\cdot P^{-1}")
	with PrintEquation() as p:
		print("\\exp\\mathbf{A} = P\\cdot \\exp D \\cdot P^{-1}")
	with PrintEquation() as p:
		print("\\Phi(\\tau) = \\exp\\{A\\cdot \\tau\\}")
	with PrintEquation() as p:
		print("\\mathbf{X} = \\Phi(t)\\cdot\\mathbf{X}(0)+\\int_0^t \\Phi(t-\\tau)\\cdot G(t) d\\tau")
	with PrintEquation() as p:
		print("\\mathbf{Y}(t) = C\\cdot \\mathbf{X}(t)")

	print("<br>")
	print("<br>")

	# Вывод решения
	with PrintEquation() as p:
		print("\\mathbf{P} = ", latex(P))
	with PrintEquation() as p:
		print("\\mathbf{D} = ", latex(D))
	with PrintEquation() as p:
		print("\\mathbf{P}^{-1} = ", latex(P1))
	with PrintEquation() as p:
		print("\\exp \\mathbf{D} = ", latex(DE))
	with PrintEquation() as p:
		print("\\exp \\mathbf{A} = ", latex(AE))
	with PrintEquation() as p:
		print("\\Phi(\\tau) = ", latex(F))
	with PrintEquation() as p:
		print("\\Phi(t)\\cdot\\mathbf{X}(0) = ", latex(FX0))
	with PrintEquation() as p:
		print("\\Phi(t-\\tau)\\cdot G(t) = ", latex(FG))
	with PrintEquation() as p:
		print("\\int_0^t \\Phi(t-\\tau)\\cdot G(t) d\\tau = ", latex(FI))
	with PrintEquation() as p:
		print("\\mathbf{X} = ", latex(X))
	with PrintEquation() as p:
		print("\\mathbf{Y} = ", latex(Y))
