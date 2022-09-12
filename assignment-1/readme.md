## Tilbakemelding
Hei, her er en liten tilbakemelding på obligen:)

### Oppgave 1:
Du kjører gråtonetransformen med std 67, men dere skulle ha 64. Ellers en fin funksjon!

I punktene dine x,y har du glemt at vi regenr x som vertikal akse. Så alle dine x,y bør egt være y,x.

Bra forlengs mapping, og baklengs og interpolasjoner! Fine diskusjoner også her!

Men ikke plott med aspect='auto', det ødelegger formen på bildet.

### Oppgave 2:
Veldig bra konvolusjon! Eneste er at filteret bør kunne være feks 5x3, ikke bare nxn.
- Dette må jeg sjekke

Gauss filteret er fint utifra oppgaveteksten til 2017, men dere skulle bruke årets formel som er litt annerledes.
- Her mener hun at jeg skulle finne A. Mulig jeg kan fikse dette

Dere skulle heller ikke bruke Sobel, men 1d symmetrisk for å finne gradienten. Ellers fine!
- Hva menes med 1D symmetrisk, trodde det va det jeg gjorde med Sobel 1D.


I tynningen skal du ikke trenge å padde gradientene. 
- Dette må jeg se nærmere på

Det er også litt småfeil ellers i algoritmen din:
Poenget er at dersom vår piksel har gradient i en gitt retning, vil vi tynne i denne retningen, og 180 grader på retningen - altså uavhengig av retningen til pikslene rundt!
- Igjen, dette må jeg fikse.

I tillegg setter du verdien i i-1, j-1 til null, ikke bare i,j som er det du egentlig sjekker.
- Her tror jeg retter har bommet. Verdiene settes til i-1 og j-1 fordi jeg bruker et større array (padded) i forløkken. 

Ellers er det riktige retninger osv!

I hysteresetersklingen skjekker du bare om piksler har sterke naboer en gang, og får
derfor ikke markert naboer av svake piksler som er naboer av sterke piksler.
Fine refleksjoner generelt

Ellers har du en fin oppgave!