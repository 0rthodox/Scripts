from math import sin


def f(x):
    return sin(100 * x) / (1 + x ** 2)


def integrate(f, x0, x, h):
    xs = [x0 + h * i for i in range(int((x - x0) / h))]
    result = 0
    for xi in xs:
        result += f(xi) * h
    return result


from math import sqrt


def gauss2(f, a, b):
    diff = (b - a) / 2
    summ = (b + a) / 2
    return diff * (f(summ - diff / sqrt(3)) + f(summ + diff / sqrt(3)))


def integrategauss(f, x0, x, h):
    xs = [x0 + h * i for i in range(int((x - x0) / h) + 1)]
    result = 0
    for i in range(1, len(xs)):
        result += gauss2(f, xs[i - 1], xs[i])
    return result


H = 0.000001
Ih = integrate(f, 0, 1, H)
I2h = integrate(f, 0, 1, 2 * H)
print("М. Ньютона-Котеса:")
print(f"Ih = {Ih}, I2h = {I2h}, Δ = {abs(I2h - Ih)}")
Hg = 0.000001
print("М. Гаусса:")
print(f"I = {integrategauss(f, 0, 1, Hg)}")
