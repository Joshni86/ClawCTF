#!/bin/bash
echo "=== Decompiling Challenge ==="
echo ""
echo "Using javap to disassemble:"
echo ""
echo "FlagParts.class:"
javap -c -cp ClawCTF_Challenge.jar FlagParts | head -50
echo ""
echo "RealDecryptor.class:"
javap -c -cp ClawCTF_Challenge.jar RealDecryptor | head -30
