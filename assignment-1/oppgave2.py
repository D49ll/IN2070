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

def padding_nearest_neighbor(img, zeros = False):
    img = np.pad(img,pad_width=1)

    if zeros:
        return img

    rows, col = img.shape
 
    #Hjørnene settes
    img[0,0] = img[1,1]
    img[0,-1] = img[1,-2]
    img[-1,0] = img[-2,1]
    img[-1,-1] = img[-2,-2]

    #Øvre og nedre rad settes
    for i in range(1,col-1):
        img[0,i] = img[1,i] #Øverste rad
        img[-1,i] = img[-2,i] #Nederste rad

    #Venstre og høyre kolonner settes
    for i in range(1,rows-1):
        img[i,0] = img[i,1]
        img[i,-1] = img[i,-2]

    return img

def conv3x3(img,kernel,zeros=False):
    rows, col = img.shape
    img_conv = np.zeros((rows,col))
    kernel = np.rot90(kernel,2)

    img = padding_nearest_neighbor(img,zeros)
    for r in range(rows):
        for c in range(col):
            overlay = img[r:3+r,c:3+c] #Finner 3x3 overlay fra originalbildet, der senterpixelen er første piksel i bildet.
            conv_val = np.sum(np.multiply(kernel,overlay)) #Multipliserer elementvis og summerer
            img_conv[r,c] = conv_val
    
    return img_conv

def subplot_result(img1, img2):
    fig, ax = plt.subplots(1,2)
    ax[0].imshow(img1,cmap='gray',vmin=0,vmax=255,aspect='auto')
    ax[0].set_title('Original')
    ax[1].imshow(img2,cmap='gray',vmin=0,vmax=255,aspect='auto')
    ax[1].set_title('Convoluted')
    fig.tight_layout()
    plt.show( )

def oppgave2_1():
    img = imread('portrett_standardisert.png',as_gray=True)
    middelverdi = np.ones((3,3)) * 1/9
    img_conv = conv3x3(img,middelverdi)
    subplot_result(img, img_conv)

def oppgave2_2():
    pass

def main():
    oppgave2_1()

main()

