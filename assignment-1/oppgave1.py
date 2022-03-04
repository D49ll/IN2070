import matplotlib.pyplot as plt
import numpy as np
from imageio import imread, imwrite
import math

def find_std_mean(f):
    # middelverdi = summen av alle pikselverdier / antall piksler
    # varians = summen av (hver pikselverdier - middelverdi)^2/ antall piksler 
    # standardavvik = kvadratroten av varians

    n,m = f.shape
    
    #Finner middelverdi til bildet
    sum_intensity = 0
    for i in range(n):
        for j in range(m):
            sum_intensity += f[i,j]
    imean = sum_intensity/(n*m)

    #Finner varians til bildet
    sum_varians = 0
    for i in range(n):
        for j in range(m):
            sum_varians += (f[i,j]-imean)**2
    varians = sum_varians/(n*m)

    #Finner standardavvik til bildet
    std = math.sqrt(varians)
    
    return std, imean

def linear_graytransform(f,std_T,imean_T):
    #Anta en lineær gråtone-transform T[i] = ai + b
    # a = (ønsket standardavvik) / (faktisk standardavvik)
    # b = (ønsket middelverdi) - a * (faktisk middelverdi)
    #NB: bildet skal kunne representeres med 8 bit, dvs 0-255 ulike gråtoner.
    #    alt over 255 og under 0 må derfor klippes.
    
    #Grenser for klipping
    maxT = 255
    minT = 0

    #Antall piksler i bildet
    n,m = f.shape

    #Finner standardavvik og middelverdi til originalbilde
    std, imean = find_std_mean(f)

    #Uttrykker a og b med hensyn på ønsket standardavvik og middelverdi
    a = std_T / std
    b = imean_T - a*imean

    #Transformerer pikselintensitet i hver piksel fra originalbilde 
    f_standard = np.zeros((n,m))
    f_standard_limited = np.zeros((n,m))

    for i in range(n):
        for j in range(m):
            T = a*f[i,j]+b
            f_standard[i,j]  = T
            if T > maxT:
                T = 255
            elif T < minT:
                T = 0
            f_standard_limited[i,j] = T 
        
    return f_standard_limited, f_standard

def find_constants_from_coordinates(from_coord, to_coord):
    x1 = from_coord[0,0]
    y1 = from_coord[0,1]
    x2 = from_coord[1,0]
    y2 = from_coord[1,1]
    x3 = from_coord[2,0]
    y3 = from_coord[2,1]

    x1_m = to_coord[0,0]
    y1_m = to_coord[0,1]
    x2_m = to_coord[1,0]
    y2_m = to_coord[1,1]
    x3_m = to_coord[2,0]
    y3_m = to_coord[2,1]


    #Using these points we can model a linear system as Cz = d 
    #and solve for 6 unknowns finding the constant factors of the affine transform
    
    #Finding the coefficient matrix, C
    C = np.array([
        [x1, y1, 1, 0, 0, 0],
        [0, 0, 0, x1, y1, 1],

        [x2, y2, 1, 0, 0, 0],
        [0, 0, 0, x2, y2, 1],

        [x3, y3, 1, 0, 0, 0],
        [0, 0, 0, x3, y3, 1],
    ])

    #Constant vector, d
    d = np.array([x1_m,y1_m, x2_m,y2_m, x3_m,y3_m])
    
    #Solving the linear system: Cz = d
    return np.linalg.solve(C,d)

def affine_transform(x,y, constants, inverse = False):
    a = np.array([constants[0],constants[1],constants[2]])
    b = np.array([constants[3],constants[4],constants[5]])

    A = np.array([
        [a[0],a[1],a[2]],
        [b[0],b[1],b[2]],
        [0, 0, 1]
        ])
    b = np.array([x,y,1])
    
    if inverse:
        #Inverse mapping
        #Perform matrix multiplication: A⁻1 * b = (x,y)
        x_m,y_m,_ = np.dot(np.linalg.inv(A),b)
    else:
        #Forward mapping
        #Perform matrix multiplication: A * b = (x,y)
        x_m,y_m,_ = np.dot(A,b)

    return x_m,y_m

def forward_mapping(img,mask,from_coord,to_coord):
    y_axis_mask,x_axis_mask = mask.shape
    y_axis_img,x_axis_img= img.shape
    affine_constans = find_constants_from_coordinates(from_coord,to_coord)
    img_reshaped = np.zeros((y_axis_mask,x_axis_mask))
    
    for y in range(y_axis_img):
        for x in range(x_axis_img):
            x_m, y_m = affine_transform(x,y,affine_constans)
            x_m = round(x_m)
            y_m = round(y_m)
            if (0 <= x_m < x_axis_mask) and (0 <= y_m < y_axis_mask):
                img_reshaped[y_m, x_m] = img[y,x]

    print("\nPixel information (forward mapping):")
    print(f"Original image: {x_axis_img}x{y_axis_img}")
    print(f"Mask:           {x_axis_mask}x{y_axis_mask}")
    print(f"Reshaped image: {x_axis_mask}x{y_axis_mask}")

    return img_reshaped

def nearest_neighbor(img,mask,from_coord,to_coord):
    #Finds the pixel intensity of the nearest pixel found from the inverse transform
    y_axis_mask,x_axis_mask = mask.shape
    y_axis_img,x_axis_img= img.shape
    affine_constans = find_constants_from_coordinates(from_coord,to_coord)
    img_reshaped = np.zeros((y_axis_mask,x_axis_mask))

    for y_m in range(y_axis_mask):
        for x_m in range(x_axis_mask):
            x, y = affine_transform(x_m,y_m,affine_constans,inverse = True)
            
            #Nearest neighbor (i.e find intensity of nearest pixel)
            x = round(x)
            y = round(y)

            if(0 <= x < x_axis_img) and (0 <= y < y_axis_img):
                img_reshaped[y_m,x_m] = img[y,x]
    
    print("\nPixel information (nearest neighbor):")
    print(f"Original image: {x_axis_img}x{y_axis_img}")
    print(f"Mask:           {x_axis_mask}x{y_axis_mask}")
    print(f"Reshaped image: {x_axis_mask}x{y_axis_mask}")

    return img_reshaped

def bilinear_interpolation(img,mask,from_coord,to_coord):
    #Find the pixel intensity based of 4 nearest pixels in original image
    y_axis_mask,x_axis_mask = mask.shape
    y_axis_img,x_axis_img= img.shape
    affine_constans = find_constants_from_coordinates(from_coord,to_coord)
    img_reshaped = np.zeros((y_axis_mask,x_axis_mask))

    for y_m in range(y_axis_mask):
        for x_m in range(x_axis_mask):
            x, y = affine_transform(x_m,y_m,affine_constans,inverse = True)
            
            #Bilnear interpolation
            x0 = math.floor(x)
            y0 = math.floor(y)
            x1 = math.ceil(x)
            y1 = math.ceil(y)
            if((0 <= x0 < x_axis_img) and (0 <= y0 < y_axis_img)) and ((0 <= x1 < x_axis_img) and (0 <= y1 < y_axis_img)):
                dx = x-x0
                dy = y-y0

                p = img[y0,x0] + (img[y0,x1]-img[y0,x0])*dx
                q = img[y1,x0] + (img[y1,x1]-img[y1,x0])*dx

                img_reshaped[y_m,x_m] = p + ((q-p)*dy)
               
    print("\nPixel information (bilinear interpolation):")
    print(f"Original image: {x_axis_img}x{y_axis_img}")
    print(f"Mask:           {x_axis_mask}x{y_axis_mask}")
    print(f"Reshaped image: {x_axis_mask}x{y_axis_mask}")

    return img_reshaped


def oppgave1_1():
    #Oppgave 1.1: Preprosessering av protrett
    # Standardisere kontrasten. Det prosesserte bilde skal ha en middelverdi(imean_T) lik 127
    # og et standardavvik (std_T) lik 67. Bilde skal kunne lagres med 8bit, det betyr at
    # bilde skal ha pikselintensiteter mellom 0 og 255.
    # Ønsker å gjøre dette ved å bruke en linear endring

    f = imread('portrett.png',as_gray=True)

    #Lineartransformerer bilde med ønsket standardavvik og middelverdi
    f_limited, f_not_limited = linear_graytransform(f,std_T = 67, imean_T = 127)

    #Ønsker å sjekke av vi faktisk oppnådde ønsket standardavvik og middelverdi
    #For å gjøre det regner jeg ut for originalbildet og for det behandlede bildet (uten grenser)
    #Dersom jeg hadde brukt det behandlede bildet med grenser ville vi ikke fått riktig resultat
    std_original, mean_original = find_std_mean(f)
    std_transform, mean_transform = find_std_mean(f_not_limited)
    std_transform_limit, mean_transform_limit = find_std_mean(f_limited)


    #Visualisering
    plt.imshow(f,cmap='gray',aspect='auto')
    plt.title(f'Originalbilde\nstandardavvik={round(std_original,2)} og middelverdi={round(mean_original,2)}')

    plt.figure()
    plt.imshow(f_limited,cmap='gray',aspect='auto')
    plt.title(f'Standardisert\nuten grenser: standardavvik={round(std_transform,2)} og middelverdi={round(mean_transform,2)}\n\
        med grenser: standardavvik={round(std_transform_limit,2)} og middelverdi={round(mean_transform_limit,2)}')

    plt.show()

    imwrite('portrett_standardisert.png',f_limited.astype(np.uint8))

def oppgave1_2():
    mask = imread('geometrimaske.png',as_gray=True)
    img = imread('portrett_standardisert.png',as_gray=True)

    #Portrett.png: 
    #left eye = (86,89)
    #right eye = (119,67)
    #center of mouth = (129,109)
    img_coord = np.array([
        [86,89],
        [119,67],
        [129,109]
    ])

    #Geometrimaske.png:
    #left eye = (171,258) 
    #right eye = (344,259) 
    #center of mouth = (258,441)
    mask_coord = np.array([
        [171,258],
        [344,259],
        [258,441] 
    ])

    img_forward = forward_mapping(img,mask,img_coord,mask_coord)
    img_nearest_neighbor = nearest_neighbor(img,mask,img_coord,mask_coord)
    img_bilinear_interpolation = bilinear_interpolation(img,mask,img_coord,mask_coord)

    imwrite('portrett_forlengsmapping.png',img_forward.astype(np.uint8))
    imwrite('portrett_nærmeste-nabo.png',img_nearest_neighbor.astype(np.uint8))
    imwrite('portrett_bilinær-interpolasjon.png',img_bilinear_interpolation.astype(np.uint8))

    #Visualisering
    plt.imshow(img,cmap='gray',aspect='auto')
    plt.title('Original bilde')

    plt.figure()
    plt.imshow(img_forward, cmap='gray',aspect='auto')
    #plt.imshow(mask, cmap='gray', alpha=.1,aspect='auto')
    plt.title('Forlengs-mapping')

    plt.figure()
    plt.imshow(img_nearest_neighbor, cmap='gray',aspect='auto')
    #plt.imshow(mask, cmap='gray', alpha=.4,aspect='auto')
    plt.title('Nærmeste nabo')

    plt.figure()
    plt.imshow(img_bilinear_interpolation, cmap='gray',aspect='auto')
    #plt.imshow(mask, cmap='gray', alpha=.4,aspect='auto')
    plt.title('Bilineær interpolasjon')
    plt.show()


def main():
    oppgave1_1()
    oppgave1_2()

main()