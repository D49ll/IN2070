'''
Programmer en generell implementasjon av konvolusjon av et bilde med et konvolusjonsfilter

Konvolusjonsfilter: 
1. Roter middelverdifilteret med 180 grader mot klokken
2. Legg det roterte filteret over første posisjon der filteret og innbildet overlapper
3. Multipliser filterets vekter med verdiene av de overlappede pikslene
4. Resultatet kalles responsen av filteret
5. Gjenta steg 4 for alle overlappene i innbildet

NB! - Naboskapet er rektangulært med odde lengder, som betyr at alltid vil ha partall med verdier rundt senterpikselen
    - Antar også at origio er i senterpikselen
    - Ut-bilde skal ha samme størrelse som innbildet
    - Bilderanden skal utvides med nærmeste pixel
'''
import matplotlib.pyplot as plt
import numpy as np
from imageio import imread

def padding(img,kernel_size, zeros = False):
    k = (kernel_size-1)//2
    padded = np.pad(img,k)

    #Dersom vi ønsker at bilderanden skal ha pikselverdi lik 0
    if zeros:
        return padded

    rows, col = padded.shape
    #Hjørnene paddes til nærmeste nabo's pikselverdi
    padded[0:k,0:k] = padded[k,k] #Øverst venstre
    padded[rows-k:,0:k] = padded[rows-k-1,k]#Nederst venstre
    padded[0:k,col-k:] = padded[k,col-k-1]#Øverst høyre
    padded[rows-k:,col-k:] = padded[rows-k-1,col-k-1]#Nederst høyre
  
    #Øvre og nedre rad paddes til nærmeste nabo's pikselverdi
    for i in range(k,rows+k):
        padded[0:k,i] = padded[k,i] #Øverste rad
        padded[rows-k:,i] = padded[rows-k-1,i] #Nederste rad

    # #Venstre og høyre kolonner paddes til nærmeste nabo's pikselverdi
    for i in range(k,rows-k):
        padded[i,0:k] = padded[i,k] #Venstre kolonne
        padded[i,col-k:] = padded[i,col-k-1]#Høyre kolonne

    return padded

def convolution(img,kernel,zeros=False):
    rows, col = img.shape
    img_conv = np.zeros((rows,col))
    kernel_size = kernel.shape[0]
    kernel = np.rot90(kernel,2)

    #For å oppnå "same convolution", at inn og utbilde har samme størrelse, må legge til padding på innbilde
    img = padding(img,kernel_size,zeros)
    for r in range(rows):
        for c in range(col):
            overlay = img[r:kernel_size+r, c:kernel_size+c]
            img_conv[r,c] = np.sum(kernel * overlay) #for np.arrays er '*'-operatoren det samme som elementvis matrisemultiplikasjon
    
    return img_conv

def subplot_result(img1, img2,kernel_type):
    fig, ax = plt.subplots(1,2)
    ax[0].imshow(img1,cmap='gray',vmin=0,vmax=255,aspect='auto')
    ax[0].set_title('Original')
    ax[1].imshow(img2,cmap='gray',vmin=0,vmax=255,aspect='auto')
    ax[1].set_title('Convoluted using '+kernel_type)
    fig.tight_layout()
    plt.show( )

def gaussian_kernel(sigma):
    kernel_size = 1 + round(sigma*8)
    h = np.ones((kernel_size, kernel_size))
    m = kernel_size//2

    for x in range(kernel_size):
        for y in range(kernel_size):
            #Usikker på hvordan vi skal finne A
            A = 1/(2*np.pi*sigma**2)
            exp = np.exp(-((x-m)**2 + (y-m)**2)/(2*sigma**2))
            h[x,y] = A*exp
    return h

def average_kernel(n):
    return np.ones((n,n)) * 1/(n**2)


def oppgave2_1():
    img = imread('cellekjerner.png',as_gray=True)
    
    average = average_kernel(7)
    
    img_conv = convolution(img,average)
    
    subplot_result(img, img_conv,"average 25x25 kernel")

def oppgave2_2():
    img = imread('cellekjerner.png',as_gray=True)

    sigma = 2
    gaussian = gaussian_kernel(sigma)
    img_conv = convolution(img, gaussian)
    subplot_result(img, img_conv,f"gaussian with sigma {sigma}")

def main():
    np.set_printoptions(threshold=np.inf)
    
    oppgave2_2()

main()

