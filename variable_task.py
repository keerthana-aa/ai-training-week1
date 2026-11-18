a = 10
b = 3.5
c = "Python"
d = [1, 2, 3]
e = {"name": "Ravi", "age": 22}
f = {1, 2, 3}
g = (1, 2, 3)

print(a, type(a))
print(b, type(b))
print(c, type(c))
print(d, type(d))
print(e, type(e))
print(f, type(f))
print(g, type(g))

sales = [12000, 0, 8500, 15000, -200, 9800]
total = 0

for s in sales:
    if s <= 0:
        print("Skipped invalid value", s)
        continue
    total += s
    print("Added", s, "total", total)
    if total > 30000:
        break

if total > 30000:
    print("Target reached. Stopped at", total)
else:
    print("Target not reached")