#Imports for oppgave1
import matplotlib.pyplot as plt
import numpy as np
from imageio import imread

#Imports for oppgave2
import math

def oppg1():
    '''
    Skriv et program som leser inn bildet mona.png, regner ut differansen mellom nabo-piksler, 
    og viser resultatet som et bilde på skjermen. Altså vil resultat-bildet være:

        f_out(i,j) = f(i,j) - f(i-1,j)

    image()-kommandoen viser negative verdier som sort, 
    så prøv å vise bildet med en bias på feks. 128. (Legg 128 til hver piksel).

    Prøv å multiplisere f_out med en faktor større enn 1, hva skjer med kontrasten i resultatbildet da?
    '''

    #Import av bilde
    filename = 'img/mona.png'
    f = imread(filename,as_gray=True)
    plt.imshow(f,cmap='gray')
    plt.title('Originalbilde')

    #Behandle bilde
    brightness = 128
    contrast = 1.5
    N,M = f.shape #Finner antall pixler

    f_out = np.zeros((N,M))
    f_out_brightness = np.zeros((N,M))
    f_out_contrast = np.zeros((N,M))

    for i in range(N):
        for j in range(M):
            f_out[i,j] = f[i,j] - f[i-1,j]

    f_out_brightness = f_out + brightness
    f_out_contrast = contrast * f_out

    #Visualisering 
    plt.figure()
    plt.imshow(f_out,cmap='gray',vmin=0,vmax=255,aspect='auto')
    plt.title('f_out')

    plt.figure()
    plt.imshow(f_out_brightness,cmap='gray',vmin=0,vmax=255,aspect='auto')
    plt.title('f_out_brightness: '+str(brightness))

    plt.figure()
    plt.imshow(f_out_contrast,cmap='gray',vmin=0,vmax=255,aspect='auto')
    plt.title('f_out_contrast: '+str(contrast))

    plt.show()

def minste_y(D, s, lamb):
    return (math.tan(1.22*(lamb/D))*s)

def y_merket(y,s,f):
   return (y*f)/(s-f)

def f_max(T_min):
    return 1 / T_min

def oppg2():
    '''
    Anta at vi bruker en ("perfekt") linse med aperturediameter D = 10 mm og 
    fokallengde ("brennvidde") f = 50 mm. La avstanden fra linsen til det vi 
    avbilder være s = 5 meter. Benytt bølgelengde (lambda) på 500 nanometer.
    (Det kan være en ide å se på side 8 i forelesningsnotatene for 2022.)

    a) Hva er minsteavstanden y, ifølge rayleigh-kriteriet, mellom to punkter som kan avskilles?

    Svar:   Dersom man antar at linsen er "perfekt" betyr det at vi kun trenger å ta høyde
            diffraksjon. Med det menes det at avbildingsystemer et begrenset av diffraksjon.
            Diffraksjon betyr at bilde kommer gjennom en f.eks en linse og spres i bølger

            Minsteavstander y forteller noe om detaljnivå vi kan oppnå med vårt system.

            Videre vet vi for små vinkler:
                tan v = sin v = v.
            
            rayleigh formel
                tan v = sin v = v = 1.22 lambda / D

            Fra tegning (forelsning uke 1):
            
            tan v = y / s -> y = tan v * s
    '''
    #Variabler
    D = 10* (10 ** -3)
    f = 50* (10 ** -3)
    s = 5
    lamb = 500 * (10 ** -9)
    
    #Funksjoner
    y = minste_y(D,s,lamb)
    y_mm = round(y * 10**3, 3)

    Y = y_merket(y,s,f)
    Y_um = round(Y * 10**6, 3)
    
    fmax = f_max(Y)
    fmax_kHz = round(fmax * 10**-3,3)
    
    print("Oppgave 2")
    print(f"a) y = {y_mm} mm")
    print(f"b) y' = {Y_um} um")
    print(f"d) T_min = {Y_um} um og f_max = {fmax_kHz}kHz")

def main():
    oppg2()

main()