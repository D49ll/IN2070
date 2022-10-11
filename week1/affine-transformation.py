#translation, rotation, tranlation
import math

def translation(a, b):
    return a + b

def x_rotation(theta, x0, x1, y0, y1):
    return (math.cos(theta)*(x0+x1))-(math.sin(theta)*(y0+y1))

def y_rotation(theta, x0, x1, y0, y1):
    return (math.sin(theta)*(x0+x1))+(math.cos(theta)*(y0+y1))

