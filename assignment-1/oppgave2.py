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
from pandas import Index

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
    for i in range(k,col-k):
        padded[0:k,i] = padded[k,i] #Øverste rad
        padded[rows-k:,i] = padded[rows-k-1,i] #Nederste rad
    # #Venstre og høyre kolonner paddes til nærmeste nabo's pikselverdi
    for i in range(k,rows-k):
        padded[i,0:k] = padded[i,k] #Venstre kolonne
        padded[i,col-k:] = padded[i,col-k-1]#Høyre kolonne

    return padded

def convolution(img,kernel,zeros=False,conv_1D=False):
    rows, col = img.shape
    img_conv = np.zeros((rows,col))
    kernel_size = kernel.shape[0]
    #kernel = np.rot90(kernel,2)

    #For å oppnå "same convolution", at inn og utbilde har samme størrelse, må legge til padding på innbilde
    img = padding(img,kernel_size,zeros)
    
    if conv_1D:
        hori = np.zeros((rows,col))
        vert = np.zeros((rows,col))

        pad = (kernel_size-1)//2
        #Horiosental convolution
        for r in range(pad,rows+pad):
                for c in range(col-pad-1):
                    hori[r-pad,c] = np.sum((img[r,c:c+kernel_size])*kernel[:,0])
        
        #img = padding(hori,kernel_size,zeros)
        #vertical convolution
        for c in range(pad, col+pad):
            for r in range(rows-pad-1):
                vert[r,c-pad] = np.sum((img[r:r+kernel_size,c])*kernel[0,:])
    
        img_conv = hori+vert
    else:
        for r in range(rows):
            for c in range(col):
                overlay = img[r:kernel_size+r, c:kernel_size+c]
                img_conv[r,c] = np.sum(kernel*overlay) #for np.arrays er '*'-operatoren det samme som elementvis matrisemultiplikasjon
    
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

def sobel(img):
    hy = np.array([
         [1,2,1],
         [0,0,0],
         [-1,-2,-1]
    ])
    hx = np.array([
         [-1,0,1],
         [-2,0,2],
         [-1,0,1]
    ])
    gaussian = gaussian_kernel(1)
    img_blur = convolution(img, gaussian, zeros=True)
    img_x = convolution(img_blur,hx,zeros=True,oneDimension=True)
    img_y = convolution(img_blur,hy,zeros=True,oneDimension=True)

    img_conv = img_x+img_y

    return img_conv

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

    np.set_printoptions(threshold=np.inf)
    img = imread('uio.png',as_gray=True)
    gauss_kernel = gaussian_kernel(2)
    img_blur = convolution(img,gauss_kernel)
    kernel = np.array([
         [1,2,1],
         [0,0,0],
         [-1,-2,-1]
    ])
    
    test = np.ones((10,10))
    print(test)
    for r in range(test.shape[0]):
        for c in range(test.shape[0]):
            test[r,c] = np.sum(test[r,c:c+test.shape[0]]*kernel[0,:])
    print(test)

def main():
    original = np.array([
        [50,50,100,100],
        [50,50,100,100],
        [50,50,100,100],
        [50,50,100,100],
        [50,50,100,100]
    ])
  
    img = imread('google.png',as_gray=True)
    hy = np.array([
         [1,0,-1],
         [2,0,-2],
         [1,0,-1]
    ])
    hx = np.array([
         [1,2,1],
         [0,0,0],
         [-1,-2,-1]
    ])
    hx_rot = np.rot90(hy,2)
    hor = hy[0,::-1] #Rotert 180*
    ver = hy[::-1,0] #Rotert 180*
    print(hor)
    print(ver)
    

    #ver = hx_rot[:,0]

    #print(img2)
    img2 = np.copy(original)
    conv1 = np.zeros(img2.shape)
    conv2 = np.zeros(img2.shape)


    # conv2 = np.zeros(img2.shape)
    # conv = np.zeros(img2.shape)

    img2 = padding(img2, 3, zeros=False)
    print(img2)
    for r in range(img2.shape[0]-2):
        for c in range(img2.shape[1]-2):
            print(np.sum(hor*img2[r+1,c:c+3]))
            conv2[r,c]=(np.sum(hor*img2[r+1,c:c+3]))

    conv2 = padding(conv2, 3, zeros=False)
    for r in range(conv2.shape[0]-2):
        for c in range(conv2.shape[1]-2):
            conv1[r,c]=(np.sum(ver*conv2[r:r+3,c+1]))
    print(conv1)

    Gx = convolution(original,hx,zeros=False)
    Gy = convolution(original,hy,zeros=False)
    #print(Gx)
    print(Gy)

main()

