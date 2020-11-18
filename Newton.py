import numpy

def finite_subtract(x1, f1, x2, f2):
    return (f2 - f1) / (x2 - x1)


grid = [i for i in range(7)]
values = [5, 3,11,17,-15,-145,-457]

len = len(grid)

M = numpy.zeros((len, len))

for i in range(len):
    for j in range(len - i):
        if i == 0:
            M[j, i] = values[j]
        else:
            x1 = grid[j]
            x2 = grid[j + i]
            f1 = M[j, i - 1]
            f2 = M[j + 1, i - 1]
            M[j, i] = finite_subtract(x1, f1, x2, f2)

b = M[0, :]

# print("Коэффициенты b многочлена в форме Ньютона:\n", *b)

polynomials = [numpy.poly1d([1, - x]) for x in grid[:-1]]

result = numpy.poly1d([b[0]])

for idx, val in enumerate(b[1:]):
    item = polynomials[idx] * val
    for i in range(idx):
        item *= polynomials[i]
    result = item + result

print('Интерполяционный многочлен в классической форме:', result, sep='\n')

# x = 1.55
# print(f'Значение в точке {x}:', result(x), sep='\n')