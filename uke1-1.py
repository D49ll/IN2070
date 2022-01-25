import matplotlib.pyplot as plt
import numpy as np
from imageio import imread

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