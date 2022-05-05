'''
A common file for functions used to solve assignment 2 in IN2070
'''

import numpy as np

def my_pad(f,h):
    row, col = f.shape
    k = (row//2) - 1
    K = (col//2) - 1
    
    h_pad = np.zeros((row,col))
    h_pad[k:k+h.shape[0],K:K+h.shape[1]] = h

    return h_pad