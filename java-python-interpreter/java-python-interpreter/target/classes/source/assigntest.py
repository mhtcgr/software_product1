# test assign
def a(p):
    if p > 1:
        return p*a(p-1)
    else:
        return 1
print(a(5))
# test binop
y = (not 1) + 2
print(y)
