import math

x = [float(item.strip()) for item in input("Input x-s: ").replace(',', '.').split()]
sx = [float(item.strip()) for item in input("Input sigmaX-s: ").replace(',', '.').split()]
y = [float(item.strip()) for item in input("Input y-s: ").replace(',', '.').split()]
sy = [float(item.strip()) for item in input("Input sigmaY-s: ").replace(',', '.').split()]
sxx = [2 * s * x for s, x in zip(sx, x)]
syy = [2 * s * y for s, y in zip(sy, y)]
sxy = [x * y * math.sqrt((sx / x) ** 2 + (sy / y) ** 2) for sx, x, sy, y in zip(sx, x, sy, y)]
wx = [1 / val ** 2 for val in sx]
wy = [1 / val ** 2 for val in sy]
wxx = [1 / val ** 2 for val in sxx]
wyy = [1 / val ** 2 for val in syy]
wxy = [1 / val ** 2 for val in sxy]
xmed = sum([w * x for w, x in zip(wx, x)]) / sum(wx)
ymed = sum([w * y for w, y in zip(wy, y)]) / sum(wy)
xxmed = sum([w * x ** 2 for (w, x) in zip(wxx, x)]) / sum(wxx)
yymed = sum([w * y ** 2 for (w, y) in zip(wyy, y)]) / sum(wyy)
xymed = sum([w * x * y for (w, x, y) in zip(wxy, x, y)]) / sum(wxy)
k = (xymed - xmed * ymed) / (xxmed - xmed ** 2)
b = ymed - k * xmed
print(xmed, ymed, xxmed, yymed)
sk = math.sqrt(((yymed - ymed ** 2) / (xxmed - xmed ** 2) - k ** 2) / (len(x) - 2))
sb = sk * math.sqrt(xxmed)
print(f'k = {k}', f'sigmak = {sk}', f'b = {b}', f'sigmab = {sb}')
print(f'E = {b / k}, sigmaE = {math.sqrt((sk / k) ** 2 + (sb / b) ** 2) * b / k}')