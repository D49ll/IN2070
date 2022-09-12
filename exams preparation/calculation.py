import numpy as np
from scipy import signal



def main():
    np.set_printoptions(suppress=True)

    h = np.array([
        [1, 4, 6, 4, 1]
    ])
    

    f = np.array([
        [1, 0, -2, 0, 1]
    ])

    c1 = signal.convolve(h,np.transpose(f))
    c2 = signal.convolve(f, np.transpose(h))

    # print(f"2D conv without 'same':\n{signal.convolve(f,h)}")
    # print(f"2D conv with 'same':\n{signal.convolve(f,h, 'same')}")
    print(c1+c2)

main()