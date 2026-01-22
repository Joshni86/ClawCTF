
### `solve.py` (Auto-solver for verification)

#!/usr/bin/env python3
import subprocess
import base64
import re

def solve():
    print("=== Auto-solving Challenge ===")
    
    # Step 1: Extract from RealDecryptor
    encrypted = [0x73, 0x68, 0x69, 0x66, 0x74, 0x65, 0x64, 0x5f, 
                 0x63, 0x6f, 0x6e, 0x74, 0x72, 0x6f, 0x6c, 0x5f,
                 0x66, 0x6c, 0x6f, 0x77, 0x7d]
    key = 0x15
    part2 = ''.join(chr(b ^ key) for b in encrypted)
    print(f"Part 2 from RealDecryptor: {part2}")
    
    # Step 2: Decode FlagParts
    part_java = "wnin"[::-1]  # Reverse rot13
    part_bytecode = base64.b64decode("eWJwbnFyYm==").decode()
    part_obfuscated_bytes = [0x0C, 0x1B, 0x1A, 0x19, 0x5E, 0x5F, 0x58, 0x5B]
    part_obfuscated = ''.join(chr(b ^ 0x7F) for b in part_obfuscated_bytes)
    
    flag = f"CTF{{{part_java}{part_bytecode}{part_obfuscated}}}"
    print(f"Assembled flag: {flag}")
    
    # Step 3: Verify with FinalFlag
    print("\n=== Running FinalFlag ===")
    subprocess.run(["java", "-cp", "obfuscated.jar", "FinalFlag"])

if __name__ == "__main__":
    solve()
