# Obligatorisk oppgave 2

- [Obligatorisk oppgave 2](#obligatorisk-oppgave-2)
- [Oppgave 1 - Implementasjon av konvolusjonsfilter i frekvensdomenet](#oppgave-1---implementasjon-av-konvolusjonsfilter-i-frekvensdomenet)
  - [Generelt](#generelt)
  - [Oppgave 1.1 og 1.2](#oppgave-11-og-12)
  - [Oppgave 1.2](#oppgave-12)
- [Oppgave 2 - Ikke-tapsfri JPEG-kompresjon](#oppgave-2---ikke-tapsfri-jpeg-kompresjon)
  - [Resultatbilder](#resultatbilder)

# Oppgave 1 - Implementasjon av konvolusjonsfilter i frekvensdomenet

## Generelt
Koden ligger vedlagt delivry. For å kjøre programmet brukes følgende

```
$ python3 oppgave1.py
```

Bildene og tidskurvene lagres i mappen der `oppgave1.py` kjøres.

## Oppgave 1.1 og 1.2

Originalbildet\
<img src="./cow.png" width="700">

Resultatbilde fra romlig konvolusjon med 15x15 middelverdifilter\
<img src="./oppg1_1%20(15x15)%20cow.png" width="700">

Resultatbilde fra frekvensdomenet med 15x15 middelverdifilter\
<img src="./oppg1_1%20(fft2)%20cow.png" width="700">

## Oppgave 1.2

# Oppgave 2 - Ikke-tapsfri JPEG-kompresjon

## Resultatbilder
Originalbilde\
<img src="./uio.png" width="700">

Rekonstruert uten kvantifisering\
<img src="./uio_no_quantification.png" width="700">

Rekonstruert med kvantifiseringsfaktor q = 0.1\
<img src="./uio_reconstruction_q_0.1.png" width="700">

Rekonstruert med kvantifiseringsfaktor q = 0.5\
<img src="./uio_reconstruction_q_0.5.png" width="700">

Rekonstruert med kvantifiseringsfaktor q = 2\
<img src="./uio_reconstruction_q_2.png" width="700">

Rekonstruert med kvantifiseringsfaktor q = 8\
<img src="./uio_reconstruction_q_8.png" width="700">

Rekonstruert med kvantifiseringsfaktor q = 32\
<img src="./uio_reconstruction_q_32.png" width="700">

