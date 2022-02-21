import math

def f(x,y):
    if x == 221 and y == 396:
        return 18
    elif x==221 and y == 397:
        return 45
    elif x==222 and y == 396:
        return 52
    elif x==222 and y == 397:
        return 36
    else:
        print("feil input")

def bilinear(x, y):
    x0 = math.floor(x)
    y0 = math.floor(y)

    x1 = math.ceil(x)
    y1 = math.ceil(y)

    dx = x-x0
    dy = y-y0

    p = f(x0,y0) + (f(x1,y0)-f(x0,y0))*dx
    q = f(x0,y1) + (f(x1,y1)-f(x0,y1))*dx
    
    return p + ((q-p)*dy)

def main():
    print(f"f(x',y')={bilinear(221.3,396.7)}")

main()