#!/bin/bash
echo "=== Testing ClawCTF Challenge ==="
echo ""
echo "1. Normal run:"
java -jar ClawCTF_Challenge.jar
echo ""
echo "2. Debug mode (with hints):"
java -jar ClawCTF_Challenge.jar debug
echo ""
echo "3. Solution path:"
java -jar ClawCTF_Challenge.jar solve
echo ""
echo "4. Direct flag reveal:"
java -cp ClawCTF_Challenge.jar FinalFlag
echo ""
echo "5. Auto-solver:"
java -jar ClawCTF_Solver.jar
