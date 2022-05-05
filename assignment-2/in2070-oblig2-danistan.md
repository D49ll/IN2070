# Obligatorisk oppgave 2

- [Obligatorisk oppgave 2](#obligatorisk-oppgave-2)
- [Oppgave 1 - Implementasjon av konvolusjonsfilter i frekvensdomenet](#oppgave-1---implementasjon-av-konvolusjonsfilter-i-frekvensdomenet)
  - [Generelt](#generelt)
  - [Oppgave 1.1 og 1.2](#oppgave-11-og-12)
  - [Oppgave 1.2](#oppgave-12)
- [Oppgave 2 - Ikke-tapsfri JPEG-kompresjon](#oppgave-2---ikke-tapsfri-jpeg-kompresjon)
  - [Resultatbilder](#resultatbilder)
  - [Generelt om JPEG-kompresjon](#generelt-om-jpeg-kompresjon)
  - [a) Rekonstruksjonsfeil](#a-rekonstruksjonsfeil)
  - [b) Fremvisning av bilde](#b-fremvisning-av-bilde)
  - [Kompresjonsfaktor q og kompresjonsraten](#kompresjonsfaktor-q-og-kompresjonsraten)

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
<img src="./results/oppg1_1%20(15x15)%20cow.png" width="700">

Resultatbilde fra frekvensdomenet med 15x15 middelverdifilter\
<img src="./results/oppg1_1%20(fft2)%20cow.png" width="700">

## Oppgave 1.2

# Oppgave 2 - Ikke-tapsfri JPEG-kompresjon

## Resultatbilder
Originalbilde\
<img src="./uio.png" width="700">

Rekonstruert uten kvantifisering\
<img src="./results/uio_no_quantification.png" width="700">

Rekonstruert med kvantifiseringsfaktor q = 0.1\
<img src="./results/uio_reconstruction_q_0.1.png" width="700">

Rekonstruert med kvantifiseringsfaktor q = 0.5\
<img src="./results/uio_reconstruction_q_0.5.png" width="700">

Rekonstruert med kvantifiseringsfaktor q = 2\
<img src="./results/uio_reconstruction_q_2.png" width="700">

Rekonstruert med kvantifiseringsfaktor q = 8\
<img src="./results/uio_reconstruction_q_8.png" width="700">

Rekonstruert med kvantifiseringsfaktor q = 32\
<img src="./results/uio_reconstruction_q_32.png" width="700">

## Generelt om JPEG-kompresjon
Kompresjonsmetoden brukt i denne oppgaven er som tittelen sier ikke-tapsfri eller "lossy" kompresjon. Det er mulig å oppnå en kompresjonsrate på 30, med akseptabel reduksjon i bildekvalitet. JPEG deler innbilde opp i flere 8x8 blokker, der hver blokk transformeres med en diskret cosinus transform (DCT). Hensikten med å dele opp bilde og utføre DCT på hver blokk er å samle informasjonen til de 64 pikslene i en liten del av de 64 DCT-koeffsientene. Vi vil oppleve at flere av de 64 DCT-koeffisientene vil være tilnærmet 0, noe som gjør at vi kan komprimere bilde med koding, ofte huffmann. 

Etter 2D DCT-transformasjonen vil de høyeste verdiene finnes i øverste venstre hjørne av DCT-koeffsienetene. Verdien av koeffisientene sier noe om hvor mye hver koeffisient er tilstede i originalbilde. Vi sier pikselverdiene er transformert.

Neste steg er å dividere DCT-koeffisientene med vekt-matrise, dette gir opphav til en "lossy" kompresjon fordi vi runder til nærmeste heltll. I JPEG kompresjon er det ofte brukt en standard vekt-matrise (som også brukes i denne oppgaven). Ved å dividere på med vektmatrisen og runde til nærmeste heltall vil vi få en resultatmatrise med høye verdier i øverste venstre høyrne og resten er oftes 0. Vi sier pikselverdiene er kvantifisert.

Steget etter dette er å utføre en sikk-sakk-skanning, der de største verdiene kommer først i rekka og blir etterfulgt av flere 0'ere. En slik rekke egner seg ypperlig til å utføre løpelengdetransformasjon av de transformerte og kvantifiserte verdiene. Etterpå blir disse løpelengende kodet ved hjelp av huffman-koding. Huffman-koden og kodeboken sendes deretter til mottaker, i en komprimert tilstand. Dette ble ikke gjort i denne obligen. 

Ved å bruke kodeboken kan mottaker dekode kodeordene og reversere løpelengdetransformene. Dette vil gi mottaker samme tallrekke som ble laget i sikk-sakk-skanningen. Deretter kan mottaker mulitiplisere med samme vektmatrise (kvantifiseringen) og ender opp med samme resultat.

## a) Rekonstruksjonsfeil

"Blokk-artefakter" er et kjent fenomen når man bruker JPEG-komprimering. Denne feilen oppstår på grunn av den 8x8 blokk-oppdelingen av bildet. En annen kjent feil den såkalte Gibbs-effekten. Gibbs-effekten kan gi sløring og dobbelkonturer i skarpe kanter (endring i pikselintensitet). Disse feilene er borte i nyere standarder av JPEG kompresjon, der DCT er erstattet med "wavelets". 

Vi kan se tilfeller av disse feilene i resultatbildene. Allerede med en kompresjonsfaktor lik 2 ser man tendenser til "blokk-artefakter" i skyene og glatting. Disse feilene blir mer enda mer synlig ved kompresjonsfaktor 8 og 32, som er naturlig. Jeg observerte ikke noe form for ringing. En grunn til dette er at originalbilde i seg selv er av ganske lav oppløsning.

## b) Fremvisning av bilde
Hvilken kompresjonsfaktor som er ok for å vise bilde baserer seg veldig mye på hva bilde skal brukes til. Jeg vil si at det rekonstruerte bilde med kompresjonsfaktor lik 8 er god nok til å vise på en dataskjerm der detaljnivået ikke er viktig. Du ser tydelig hva bildet inneholder. Derimot skulle det ble vist frem der behovet for mer detaljer er tilstedet, ville jeg ikke hatt en høyere kompresjonsfaktor enn 2. 

## Kompresjonsfaktor q og kompresjonsraten

Kompresjonsraten CR er definert som forholdet mellom b; det faste antallet bits per symbol i det ukomprimerte bildet/datamengden og c; som er det gjennomsnittlige antallet bits per symbol i det komprimerte bilde/datamengden. Når c minker, dvs at vi kan representere en piksel med mindre antall bits, vil kompresjonsraten øke fordi b er en fastsatt verdi.

```
CR = b / c
```

For å finne det gjennomsnittlige antall bits per symbol en datamengde har, må man:
1. Lage en kodebok, 
   1. Finner antall forekomster, `n_i`, av symbolet `s_i` i en sekvens av `N` symboler. 
   2. Hvert symbol får sitt eget kodeord `c_i` der `b_i` er lengden av kodeordet i antall biter.
2. Alle symbolene av typen `s_i` vil dermed bidra med `n_i * b_i` biter i den totale kodesekvensen.

Når vi har et mål på antall biter brukt per symbol kan vi også finne det gjennomsnittlige antall biter per symbol i datamengden. Det gjøres ved å finne summen av alle bidragene og deretter dividere på hele sekvensen. 

```
G = range of pixelintensities
c = 0
for i=0 to G-1:
    c += b_i*n_i
c = c/N
```

La oss se på eksempelet med et gråtonebilde. Et gråtonebilde bruker 8bits per piksel, som gir b = 8. Etter en JPEG kompresjon har vi fjernet "unødig" informasjon fra bildet, gjennom kvantifiseringen. Kvantifiseringen beholder verdier som bidrar til bildets struktur, mens den fjerner mindre viktige detajler, som gjør at vi trenger mindre antall bits per piksel. Det fører til at c vil minke.

Kvantifiseringen skjer ved å dividere DCT-koeffisientene med en kjent vektmatrise. Dersom vi øker q, øker også verdiene i vektmatrisen. 

I vårt tilfellet antar vi at entropien til det komprimerte bilde tilsvarer antall bits per symbol vi får etter kompresjonen. Entropi er et matematisk mål på gjennomsnittlig informasjonsmengde i en sekvens av tall eller tegn. Det er ønskelig at det gjennomsnittlige antall biter vi bruker per symbol skal være lik entropien til meldingen.

