# Clawing at Randomness – ClawCTF

We intercepted a signing system used by a secure ClawCTF service.

The service signs messages using ECDSA over secp256k1.
However, a mysterious value is leaked with every signature.

Your task:
- Analyze the leakage
- Recover the signing key
- Obtain the flag

Files provided:
- output.txt

Rules:
- No brute forcing
- No guessing the flag
- Cryptanalysis only

Flag format:
ClawCTF{...}
