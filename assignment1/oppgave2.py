import matplotlib.pyplot as plt
import numpy as np
from imageio import imread, imwrite
import time

def angle_padding(theta_rounded):
    t = my_pad(theta_rounded,1)
    t[0,:] = -1
    t[:,0] = -1
    t[-1,:] = -1
    t[:,-1] = -1

    return t

def my_pad(img,k):
    rows = (2*k)+img.shape[0]
    col = (2*k)+img.shape[1]
    padded = np.zeros((rows,col))
    padded[k:k+img.shape[0], k:k+img.shape[1]] = img
    test = np.pad(img,k)
    assert np.array_equal(padded,test), "my_pad function returns a different array compared to np.pad()"

    return padded

def subplot_result(img1,img1_text,img2,img2_text):
    fig, ax = plt.subplots(1,2)
    ax[0].imshow(img1,cmap='gray',vmin=0,vmax=255,aspect='auto')
    ax[0].set_title(img1_text)
    ax[1].imshow(img2,cmap='gray',vmin=0,vmax=255,aspect='auto')
    ax[1].set_title(img2_text)
    fig.tight_layout()
    plt.show( )

def padding(img,kernel_size, zeros = False):
    k = (kernel_size-1)//2
    padded = my_pad(img,k)

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

    #For å oppnå "same convolution", at inn og utbilde har samme størrelse, må legge til padding på innbilde
    img = padding(img,kernel_size,zeros)
    
    if conv_1D:
        #Horisontal og vertikal vektor
        hori_vector = kernel[0,::-1] #Rotert 180*
        veri_vector = kernel[::-1,0] #Rotert 180*

        horisontal = np.zeros((rows,col))
        for r in range(rows):#img.shape[0]-2
            for c in range(col):#img.shape[1]-2
                horisontal[r,c]=(np.sum(hori_vector*img[r+1,c:c+3]))

        horisontal = padding(horisontal, kernel_size, zeros=False)
        for r in range(rows):#horisontal.shape[0]-2
            for c in range(col):#horisontal.shape[1]-2
                img_conv[r,c]=(np.sum(veri_vector*horisontal[r:r+3,c+1]))

    else:
        kernel = np.rot90(kernel,2)
        for r in range(rows):
            for c in range(col):
                overlay = img[r:kernel_size+r, c:kernel_size+c]
                img_conv[r,c] = np.sum(kernel*overlay) #for np.arrays er '*'-operatoren det samme som elementvis matrisemultiplikasjon
    
    return img_conv

def average_kernel(n):
    return np.ones((n,n)) * 1/(n**2)

def gaussian_kernel(sigma):
    kernel_size = 1 + round(sigma*8)
    h = np.ones((kernel_size, kernel_size))
    m = kernel_size//2

    for x in range(kernel_size):
        for y in range(kernel_size):
            A = 1/(2*np.pi*sigma**2)#Usikker på hvordan vi skal finne A
            exp = np.exp(-((x-m)**2 + (y-m)**2)/(2*sigma**2))
            h[x,y] = A*exp
        
    return h

def sobel(img, sigma=1,zeros=False, conv_1D=False):
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
    gaussian = gaussian_kernel(sigma)
    img_blur = convolution(img, gaussian, zeros)

    #Gradient magnitude og retning
    Gx = convolution(img_blur,hx,zeros,conv_1D)
    Gy = convolution(img_blur,hy,zeros,conv_1D)
    G = np.sqrt(Gx**2 + Gy**2)
    theta = np.arctan2(Gy,Gx)

    #Runder av til nærmeste multiplum av 45 grader, dvs vi får 4 vinkler: 0,45,90,135.
    theta_rounded = np.round(theta*(180/np.pi)*(1/45))*45 % 180
    
    #Skalerer alle gradient magnituder til grayscale
    G = G/G.max() *255

    return G, theta_rounded

def thinning_edges(Gradient, theta_rounded):
    G = np.copy(Gradient)
    G_pad = my_pad(G,1)
    A = angle_padding(theta_rounded)
    row, col = G_pad.shape
    for i in range(1,row-1):
        for j in range(1,col-1):
            #Finn retningen og magnitude til pikselen (i,j)
            angle = A[i,j].astype(int)
            magnitude = G_pad[i,j]
            
            #Horiosentale kanter (øst-vest)
            if(angle == 0):
                if(A[i-1,j] == angle and magnitude<G_pad[i-1,j]):
                    G[i-1,j-1] = 0
                    continue

                if(A[i+1,j] == angle and magnitude<G_pad[i+1,j]):
                    G[i-1,j-1] = 0
            #Vertikale kanter (nord-sør)
            elif(angle == 90):
                if(A[i,j-1] == angle and magnitude<G_pad[i,j-1]):
                    G[i-1,j-1] = 0
                    continue

                if(A[i,j+1] == angle and magnitude<G_pad[i,j+1]):
                    G[i-1,j-1] = 0
            #Skrå kanter (nordøst-sørvest)
            elif(angle == 135):
                if(A[i+1,j-1] == angle and magnitude<G_pad[i+1,j-1]):
                    G[i-1,j-1] = 0
                    continue

                if(A[i-1,j+1] == angle and magnitude<G_pad[i-1,j+1]):
                    G[i-1,j-1] = 0
                
            #Skrå kanter (nordvest-sørøst)
            elif(angle == 45):
                if(A[i-1,j-1] == angle and magnitude<G_pad[i-1,j-1]):
                    G[i-1,j-1] = 0
                    continue

                if(A[i+1,j+1] == angle and magnitude<G_pad[i+1,j+1]):
                    G[i-1,j-1] = 0
    return G

def hystere_8connectivity(strong, weak, thin_gradient):
    row, col = thin_gradient.shape
    weak_th = np.zeros((row, col))
    strong_th = np.zeros((row, col))
    discard = np.zeros((row, col))

    for i in range(row):
        for j in range(col):
            if(thin_gradient[i,j] >= strong):
                strong_th[i,j] = 255#thin_gradient[i,j]
            elif(thin_gradient[i,j]<weak):
                discard[i,j] = thin_gradient[i,j]    
            else:
                weak_th[i,j] = thin_gradient[i,j]
    
    strong_th_padded = my_pad(strong_th,1)
    row,col = strong_th_padded.shape
    for i in range(1,row-1):
        for j in range(1,col-1):
            if(weak_th[i-1,j-1]>0):
                strong_overlay = np.copy(strong_th_padded[i-1:i+2, j-1:j+2])
                if((strong_overlay>0).any()):
                    strong_th[i-1,j-1] = 25#weak_th[i-1,j-1]

    return strong_th

def oppgave2_1(filename, n):
    img = imread(filename,as_gray=True)
    average = average_kernel(n)
    img_conv = convolution(img,average)
    
    imwrite(f"cellekjerner_blur.png",img_conv.astype(np.uint8))
    # subplot_result(img,"Original image",img_conv,f"average {n}x{n} filter")

def oppgave2_2(filename, sigma, threshold_H, threshold_L):
    img = imread(filename,as_gray=True)
    gradient,gradient_ang = sobel(img,sigma,zeros=False,conv_1D=True)
    gradient_thin = thinning_edges(gradient,gradient_ang)
    canny_final = hystere_8connectivity(threshold_H,threshold_L,gradient_thin)

    imwrite(f"canny_high[{threshold_H}]_low[{threshold_L}]_sigma[{sigma}].png",canny_final.astype(np.uint8))

    #subplot_result(img,"Original image",canny_final,f"Canny filter with T_h={threshold_H} and T_l={threshold_L}")    




def main():
    start = time.time()
    oppgave2_1(filename='cellekjerner.png',n=9)
    oppgave2_2(filename='cellekjerner.png',sigma=7,threshold_H=70,threshold_L=50)

    print("image saved to folder")
    print(f"time elapsed: {round(time.time()-start)}s")
   
main()

