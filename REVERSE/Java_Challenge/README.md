\# Java Control Flow Obfuscation Challenge



\## Description

We found this suspicious Java application on a compromised server.

The developer claimed it's just a "Hello World" program, but we suspect

there's a hidden flag somewhere in the bytecode.



\## Challenge Files

\- `obfuscated.jar` - The main challenge file



\## Hints

1\. The flag is hidden using multiple layers of obfuscation

2\. Look for dead code and unused methods

3\. Control flow analysis is key

4\. Some parts need to be decrypted

5\. The flag format is: CTF{...}



\## Tools Recommended

\- JD-GUI or CFR for decompilation

\- javap for bytecode analysis

\- Your favorite text editor

\- Java Runtime Environment



\## To Run

```bash

java -jar obfuscated.jar

java -jar obfuscated.jar debug  # Try different arguments


