**Steps:**

1. Analyze the image using exiftools
2. There's a link that gives you a binary file
3. The binary flag is a .wav (`rest.wav`). You may use `bintowav.py` for this.
4. The .wav file gives a morse code which you can decrypt using https://morsecode.world/international/decoder/audio-decoder-adaptive.html
   and that gives you `CLAWCTF TH3 P455PHR4S3 15 RESTFORYOURSOUL`
5. Upload the `rest.wav` and the passphrase `RESTFORYOURSOUL` in https://futureboy.us/stegano/decinput.html to get the output.

Flag: `ClawCTF{y0u_cr4ck3d_7h3_1m463!!}`
