'''
I denne oppgaven skal du implementere de viktigste delene av ikke-tapsfri JPEG-kompresjon. Du skal lage
en funksjon (eller et program) som har to parametre:

1. Et filnavn som spesifiserer plasseringen til bildefilen som skal benyttes.
2. Ett tall q som indirekte vil bestemme kompresjonsraten.

Funksjonen skal beregne omtrentlig hvor stor lagringsplass det angitte bildet vil bruke etter JPEG-komprimering,
og finne hvilken kompresjonsrate dette tilsvarer. Vi vil anta at inputbildet er et gråtonebilde med heltallsin-
tensiteter i intervallet [0, 255] og har både en bredde og en høyde som er multipler av 8. Bruk gjerne bildet
uio.png (vist i Figur 2) for å teste implementasjonen din underveis. Fremgangsmåten du skal følge for å lage
programmet følger i oblig 2 PDF.

'''
import numpy as np
from imageio import imread
import matplotlib.pyplot as plt

def jpeg(filename, q, quantify = True):
    #Steg 1: Les inn bildet
    img = imread(filename, as_gray = True)

    #Steg 2: Subtraher 128 fra alle pikselintensiteter
    img = img - 128

    size = 8
    row, col = img.shape
    f = np.zeros((row,col))
    Q = np.array([
        [16, 11, 10, 16, 24, 40, 51, 61],
        [12, 12, 14, 19, 26, 58, 60, 55],
        [14, 13, 16, 24, 40, 57, 69, 56],
        [14, 17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77], 
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99]
    ])
    qQ = q*Q

    if(quantify):
        print(f"Starting JPEG compression for \"{filename}\" with q={q}")
    else:
        print(f"Starting JPEG compression for \"{filename}\" without quantification")

    #Transform og kvantifisering
    for x in range(0,row,size):
        for y in range(0,col,size):
            if(quantify):
                #Steg 5: Del opp bildet i 8x8 blokker og utfør 2D DCT på hver blokk, deretter punktvis divider alle 8x8 blokkene med qQ.
                f[x:x+size,y:y+size] = np.round( DCT(img[x:x+size, y:y+size]) / qQ)

            else:
                #Steg 3: Del opp bildet i 8x8 blokker og utfør 2D DCT på hver blokk
                f[x:x+size,y:y+size] = DCT(img[x:x+size, y:y+size])
    
    if(quantify):
        #Steg 6: Beregn entropien til datasettet som består av alle elementene i blokkene
        H, storage, CR, PR = compression_info(f)
        
        print(f"Find entropy of compressed image (H), storage, compressionrate (CR) and percetage removed (PR):")
        print(f"Pixel intensities range from {f.min()} to {f.max()}, which gives a range G = {(f.max()-f.min().astype(int))+1}")
        print(f"H = {np.round(H,3)}b")
        print(f"storage = {np.round(storage)}kB")
        print(f"CR = {np.round(CR,3)}")
        print(f"PR = {np.round(PR,3)}%")

    #Rekonstruering
    for u in range(0,row,size):
        for v in range(0,col,size):
            if(quantify):
                #Steg 7: Rekonstruer en tilnærming av det opprinnelige bilde
                f[u:u+size,v:v+size] = np.round( invDCT(f[u:u+size,v:v+size] * qQ) )
            else:
            #Steg 4: Rekonstruer det opprinnelige bildet ved å utføre den inverse 2D DCT på hver blokk 
                f[u:u+size,v:v+size] = np.round( invDCT(f[u:u+size, v:v+size]))
    f = f+128
    img = img+128

    if(not quantify):
        #Steg 4: Verifiser programmatisk at det rekonstruerte bildet og originalen er identisk
        print(f"Is f and img the same? {np.array_equal(img, f)}")
    
    #Steg 7: Skriv bildene til fil
    if(quantify):
        file = f'uio_reconstruction_q_{q}.png'
        plt.imsave(file, f, cmap=plt.cm.gray)

    else:
        plt.imsave('uio_no_quantification.png',f, cmap=plt.cm.gray)

    print("Successfully saved compressed image.")
    print("Compression done.")
    print()

def create_histogram(f,p,q):
    x = np.linspace(f.min().astype(int),f.max().astype(int),p.shape[0])
    plt.figure()
    plt.plot(x, p, color='r')
    plt.xlabel("Pikselintensiteter")
    plt.ylabel("Sannsynligheten for forekomst")
    plt.title(f"Normalisert histogram av JPEG kompresjon med q = {q}.")
    plt.savefig(f"histogram_q_{q}.png")
    plt.close()

def compression_info(f):
    '''
    Finner informasjon om JPEG kompresjonen
    Antar at dataforkbruket tilsvarer entropien til datasettet.
    Derfor vil H = c i dette tilfellet, der H er entropien og c er det gjennomsnittlige antall bits per symbol i den komprimerte datamengden

    '''
    p = hist(f)
    H = entropi(p)
    
    storage = (H*f.shape[0]*f.shape[1])/(8*1000) #Konverterer til kB
    CR = 8 / H #en piksel kan verdier 0-255, som tilsvarer 8 bits i naturlig binærkode
    PR = 100 * (1 - (1/CR))

    return H, storage, CR, PR
    
def c(a):
    if(a == 0):
        return 1/np.sqrt(2)
    return 1

def DCT(f):
    F = np.zeros((f.shape))
    for u in range(8):
        for v in range(8):
            F[u,v] = sum_DCT(u,v,f)
    return F

def sum_DCT(u, v, f):
    F = 0
    for x in range(8):
        for y in range(8):
            F += f[x,y] * np.cos(( (2*x+1)*u*np.pi) / 16) * np.cos(( (2*y+1)*v*np.pi) / 16)
    return 1/4*c(u)*c(v)*F
    
def invDCT(F):
    f = np.zeros((F.shape))
    for x in range(8):
        for y in range(8):
            f[x,y] = sum_invDCT(x,y,F)
    return f

def sum_invDCT(x,y,F):
    f = 0
    for u in range(8):
        for v in range(8):
            f += c(u)*c(v) * F[u,v] * np.cos(( (2*x+1)*u*np.pi) / 16) * np.cos(( (2*y+1)*v*np.pi) / 16)
    return 1/4 * f

def hist(f):
    '''
    Finner det normaliserte histogramet for f.
    
    Der vi ser på sannsynligheten for hver pikselintensitet i bilde f
    '''
    row,col = f.shape
  
    #Finner område til av pikselintensiteter
    G = 1+(f.max()-f.min()).astype(int)
    prob = np.zeros(G)
    
    #Sjekker hvert alle (x,y) i f og øker antallet for hver forekomst av aktuell intensitet
    for x in range(row):
        for y in range(col):
            prob[f[x,y].astype(int)] += 1

    #Normaliserer sannsynlighetene
    return prob/(row*col)

def entropi(p):
    '''
    Gjennomsnittlig informasjonsinnhold i sekvensen, 
    også kalt gjennomsnittlig informasjon per symbol
    Oppgitt i bits.
    '''
    G = p.shape[0]
    H = 0
    for i in range(G):
        if(p[i] == 0):
            H+=0
        else:
            H += p[i] * np.log2(p[i])
    return -H

def main():
    np.set_printoptions(suppress=True)
    filename = "uio.png"
    q_values = [0.1, 0.5, 2, 8, 32]

    jpeg(filename,0,False)

    for q in q_values:
        jpeg(filename,q)

main()
