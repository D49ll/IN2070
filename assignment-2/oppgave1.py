from math import ceil
from scipy import signal
import time
import numpy as np
from imageio import imread, imwrite
import matplotlib.pyplot as plt

def mean_value_kernel(n):
    h = (1/n**2) * np.ones([n,n]) #15x15 middelverdifilter
    return h
    
def fast_fourier(f,h):
    F = np.fft.fft2(f)  #Utfører en fast-fourier-transform på innbildet
    H = np.fft.fft2(h,(f.shape[0],f.shape[1]))  #Utfører en fast-fourier-transform på det nullutvidede filteret
    FH = np.fft.ifft2(F*H)  #Elementvis mulitipliserer i frekvensdomenet og utfører en invers-transform
    return np.real(FH)  #Returnerer kun reelle verdier

def plot_curves(y1, y2, x):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    #Setter grid og antall ticks langs aksene
    x_max = ceil(np.amax(x)/5)*5
    ax.set_xticks(np.arange(0, x_max, 5))
    ax.set_xticks(np.arange(0, x_max, 1), minor=True)

    y1_max = round(np.amax(y1),1)
    y2_max = round(np.amax(y2),1)
    y_max = y1_max if (y1_max > y2_max) else y2_max

    ax.set_yticks(np.arange(0,y_max,0.25))
    ax.set_yticks(np.arange(0,y_max,0.05), minor=True)

    ax.grid(which='both')
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)   

    #Plotter kurvene over hverandre
    plt.plot(x,y1, color='r', label='2D konvolusjon')
    plt.plot(x,y2, color='g', label='Fast-fourier-transform')

    #Plot info
    plt.xlabel("Filterstørrelse (middelverdi)")
    plt.ylabel("tid brukt (s)")
    plt.title("Prosesseringstid: 2D konvolusjon vs fast-fourier-transform")
    plt.savefig("Prosesseringstid.png")

    plt.legend()
    plt.show()

def oppgave1_1(filename):
    #Importer bildet
    f = imread(filename, as_gray = True)
    n = 15
    h = mean_value_kernel(n)
    
    #Romlig konvolusjon
    fh = signal.convolve2d(f,h,'same') #Utfører 2D konvolusjons, 'same' = fh beholder original dimensjoner

    #Frekvensdomenet
    FH = fast_fourier(f,h) 

    #Sjekker de ulike dimensjonene
    print("Bildedimensjoner:")
    print(f"Innbilde/Original: {f.shape}")
    print(f"Romlig konvolusjon: {fh.shape}")
    print(f"Frekvensdomene filtrering: {FH.shape}")

    #Lagrer bildene som gråskala
    imwrite(f'oppg1_1 ({n}x{n}) '+filename, fh.astype(np.uint8))
    imwrite(f'oppg1_1 (fft2) '+filename, FH.astype(np.uint8))
    
    # #Plotter resultatet
    # plt.imshow(FH, cmap='gray',vmin=0,vmax=255)
    # plt.title(f'fft2 {filename}')
    # plt.figure()
    # plt.imshow(fh,cmap='gray',vmin=0,vmax=255)
    # plt.title(f"({n}x{n}) {filename}")
    # plt.show()

def oppgave1_3(filename, n_tests):
    f = imread(filename, as_gray = True)

    values = np.array(list(range(1, n_tests, 2)))
    conv_time = np.zeros(values.shape)
    freq_time = np.zeros(values.shape)

    print("Starting timing process")
    for i, n in zip(range(values.shape[0]), values):
        h = mean_value_kernel(n)
        
        start = time.time()
        fh = signal.convolve2d(f,h,'same')
        conv_time[i] = time.time()-start
        
        start = time.time()
        FH = fast_fourier(f,h)
        freq_time[i] = time.time()-start

    plot_curves(conv_time,freq_time, values)

def main():
    oppgave1_1('cow.png')
    # oppgave1_2()
    # oppgave1_3('cow.png', 31)

main()