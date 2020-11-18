import numpy as np


# %%

def preprocess_data(data):
    grid = data[0, :]
    left_edges = grid[:-1]
    right_edges = grid[1:]
    return right_edges - left_edges


class Matrix:

    def __init__(self, intervals):
        self.intervals = intervals

    def get(self, i, j):
        if i >= len(self.intervals) - 1 or j >= len(self.intervals) - 1:
            raise IndexError("index ({}, {}) is out of range".format(i, j))
        elif i == j:
            return 2.0
        elif abs(i - j) > 1:
            return 0
        else:
            a1 = max(i, j)
            if j > i:
                return self.intervals[i + 1] / (self.intervals[i + 1] + self.intervals[i])
            if j < i:
                return self.intervals[i] / (self.intervals[i + 1] + self.intervals[i])


class Column:
    """ok"""

    def __init__(self, values, intervals):
        self.values = values
        self.intervals = intervals

    def get(self, i):
        if i >= len(self.intervals) - 1:
            raise IndexError('index {} is out of range'.format(i))
        u1 = (self.values[i + 1] - self.values[i]) / self.intervals[i]
        u2 = (self.values[i + 2] - self.values[i + 1]) / self.intervals[i + 1]
        return 6 * (u2 - u1) / (self.intervals[i + 1] + self.intervals[i])

    def __len__(self):
        return len(self.intervals) - 1


def forward_stage(matrix, column):
    res = np.zeros(((len(column) - 1), 2))
    res[0][0] = -matrix.get(0, 1) / matrix.get(0, 0)  # p1
    res[0][1] = column.get(0) / matrix.get(0, 0)  # q1
    #print(res[0, :])
    for i in range(1, len(column) - 1):
        ai = matrix.get(i, i - 1)
        bi = matrix.get(i, i)
        ci = matrix.get(i, i + 1)
        di = column.get(i)
        p = res[i - 1][0]
        q = res[i - 1][1]
        res[i][0] = -ci / (ai * p + bi)  # pi
        res[i][1] = (di - ai * q) / (ai * p + bi)  # qi
    return res


def back_stage(matrix, column, koef):
    m = len(column)
    res = np.zeros(m + 1)
    res[-1] = 0
    res[-2] = (column.get(m - 1) - matrix.get(m - 1, m - 2) * koef[-1][1]) / (
            koef[-1][0] * matrix.get(m - 1, m - 2) + matrix.get(m - 1, m - 1)
    )
    for i in range(m - 2, -1, -1):
        res[i] = koef[i][0] * res[i + 1] + koef[i][1]
    return res


def calculate_b(intervals, values, c):
    """ok"""
    res = np.zeros(len(intervals))
    u = (values[1] - values[0]) / intervals[0]
    res[0] = c[0] * intervals[0] / 3 + u
    for i in range(1, len(intervals)):
        u = (values[i + 1] - values[i]) / intervals[i]
        res[i] = c[i] * intervals[i] / 3 + c[i - 1] * intervals[i] / 6 + u
    return res


def calculate_d(intervals, c):
    """ok"""
    res = np.zeros(len(intervals))
    res[0] = c[0] / intervals[0]
    for i in range(1, len(intervals)):
        res[i] = (c[i] - c[i - 1]) / intervals[i]
    return res


def calculate_a(values):
    """ok"""
    res = values[1:]
    return res


def calculate(a, b, c, d, x, xi):
    res = a + b * (x - xi) + c * ((x - xi) ** 2) / 2 + d * ((x - xi) ** 3) / 6
    return res


def get_intermediate_points(a, b, c, d, x1, x2, num_points):
    grid = []
    values = []
    delta = (x2 - x1) / (num_points - 1)
    grid.append(x1)
    for j in range(1, num_points - 1):
        grid.append(x1 + delta * j)
    grid.append(x2)
    for x in grid:
        values.append(calculate(a, b, c, d, x, x2))
    return (grid, values)


# %%

data = np.zeros((2, 7))
data[0, :] = [0.87267, 1.22173, 1.57080, 1.91986, 2.26893, 2.61799, 2.9670]
data[1, :] = [0.00082, 0.01039, 0.07037, 0.32762, 1.18669, 3.59003, 9.4835]
intervals = preprocess_data(data)
grid = data[0, :]
x = data[0, :]
values = data[1, :]

m = Matrix(intervals)
col = Column(data[1, :], intervals)

c = back_stage(m, col, forward_stage(m, col))
b = calculate_b(intervals, values, c)
d = calculate_d(intervals, c)
a = calculate_a(values)

a, b, c, d = d / 6, c / 2, b, a

# print(*list(zip(a, b, c ,d)), sep='\n')


def transform(a, b, c, d, x):
    return a, b - 3 * a * x, c - 2 * b * x + 3 * a * x ** 2, d - c * x + b * x ** 2 - a * x ** 3

def transformback(a, b, c, d, x):
    b += 3 * a * x
    c += 2 * x * b - 3 * a * x ** 2
    d += c * x - b * x ** 2 + a * x ** 3
    return a, b, c, d


coeffs = []
anothercoeffs = []
leftcoeffs = []



for i in range(len(a)):
    a0, b0, c0, d0 = transform(a[i], b[i], c[i], d[i], x[i + 1])
    coeffs.append(np.poly1d([a0, b0, c0, d0]))
    anothercoeffs.append(np.poly1d([a[i], b[i], c[i], d[i]]))
    leftcoeffs.append(np.poly1d(transformback(a0, b0, c0, d0, x[i])))

def printVal(x, num):
    print(f"Значение функции в т.{x}:")
    print(coeffs[num](x))


printVal(1.55, 1)
# print("Многочлены сплайна на каждом из отрезков,\nначало координат сдвинуто в правую точку на каждом отрезке:", *anothercoeffs, sep='\n')
# print("Многочлены сплайна на каждом из отрезков,\nначало координат сдвинуто в левую точку на каждом отрезке:", *leftcoeffs, sep='\n')
# print("Многочлены сплайна на каждом из отрезков, начало координат фиксировано в нуле:", *coeffs, sep='\n')
# %%
