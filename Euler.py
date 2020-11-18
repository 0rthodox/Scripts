def f(x, y):
    return y ** 2 + (2 * x + 1 / x) * y + x ** 2


def Euler(x, y, f, h):
    f1 = f(x, y)
    f2 = f(x + h / 2, y + h * f1 / 2)
    return y + h * f2

from matplotlib import pyplot as plt

def ode(L, f):
    h = 0.4999 / L
    x = [0.5 + h * i for i in range(L + 1)]
    y = [5 / 6, ]
    for i in range(len(x) - 1):
        y.append(Euler(x[i], y[i], f, h))
    return x, y


ls = [20,]
for i in range(22):
    ls.append(ls[i] * 2)

results = []
for l in ls:
    results.append(ode(l, f))

delta = [0] + [2 ** n for n in range(len(ls))]
xn = [item[0][-1 - d] for item, d in zip(results, delta)]
yn = [item[1][-1 - d] for item, d in zip(results, delta)]
for l, xn, yn in zip(ls, xn, yn):
    print(f'L = {l}, xn = {xn}, yn = {yn}')

newH = 0.4999 / 20
xs = [0.5 + newH * i for i in range(21)]
xfinal = xs[::2]

true = results[-1][1]
trueindices = [results[-1][0].index(xi) for xi in xfinal]
for (x, y), l in zip(results[:-1], ls):
    print(f'L = {l}:')
    indices = [x.index(xi) for xi in xfinal]
    print(*[abs(y[i] - true[j]) for i, j in zip(indices, trueindices)], sep='\n')
# x2, y2 = ode(0.0002, f)
# for x, y in results:
#     plt.plot(x, y)
#     plt.show()

# plt.plot(x2, y2)
# plt.show()

# xs = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
# # indices1 = [x1.index(item) for item in xs]
# indices1 = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
# # indices2 = [x2.index(item) for item in xs]
# indices2 = [0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
# # print(indices1, indices2, sep='\n')
#
# print("Сеточная функция:")
# for i in range(11):
#     print(f'x = {xs[i]}, yh = {y1[indices1[i]]}, y2h = {y2[indices2[i]]}, Δy = {abs(y1[indices1[i]] - y2[indices2[i]])}')
