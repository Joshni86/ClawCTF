**Description**: The tracks scream DORA! They seem to be more layered than simply DORA DORA
DORA. Can you uncover the secrets within these tracks?

We are given a file `Dora.pcap`
It has an image (JPEG) and following the TCP stream (raw) reveals that there are two `ffd8` implying that there are 2 images
One image is `dora1.jpeg`
The second is `dora.jpeg`
`dora.jpeg` is dorabella cipher - https://www.dcode.fr/dorabella-cipher

Decoding will give the flag

Flag: `ClawCTF{DOYOULIKEDORACAKES}`
