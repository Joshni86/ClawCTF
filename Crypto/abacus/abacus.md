**Description** : Cats are known for their observance. First, compare the cat image's original pic and decode
the secrets it holds. Add these secrets to find the final password to the abacus. (Remember abacus may be
more than just dots and dashes.)

First inspect the `graffiti.png`
You will find :

It is actually Soroban :
https://www.dcode.fr/soroban-abacus

Each block of the the image gives a number and you add all of it : 12+345+678+8099 = 9134
9134 is the password for abacuss.jpg.bmp. Extraction should be done using `OpenStego`.
Successful extraction results in `abacus.wav`

Inspect `abacus.wav` using `Audacity` to find a code similar to morse code but it is Wabun code (Japanese morse) : https://www.dcode.fr/wabun-code
Decrypting gives `NIHON  WA  SUKOSHI  MUSUKASHI  TE゛ SU` which is Japanese for Japan is a little difficult

Flag: `ClawCTF{Japan_is_a_little_difficult}`
