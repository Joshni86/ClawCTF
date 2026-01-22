#!/bin/bash

echo "=== Building ClawCTF Java Challenge ==="
echo ""

# Clean up
rm -f *.class *.jar
rm -rf dist/

# Compile all files
echo "Compiling Java files..."
javac *.java

if [ $? -ne 0 ]; then
    echo "❌ Compilation failed!"
    exit 1
fi

echo "✅ Compilation successful!"

# Create main JAR
echo -e "\nCreating Challenge JAR..."
echo "Main-Class: Bootstrap" > manifest.txt
jar cvfm ClawCTF_Challenge.jar manifest.txt *.class

# Create solver JAR
echo "Main-Class: TestSolver" > solver_manifest.txt
jar cvfm ClawCTF_Solver.jar solver_manifest.txt *.class

# Create distribution
mkdir -p dist
cp ClawCTF_Challenge.jar dist/
cp ClawCTF_Solver.jar dist/

# Create README
cat > dist/README.md << 'EOF'
# ClawCTF: Java Bytecode Challenge

## Challenge: Control Flow Obfuscation
Find the hidden flag in the Java bytecode!

## Files:
- `ClawCTF_Challenge.jar` - The challenge file
- `ClawCTF_Solver.jar` - Auto-solver (for verification)

## How to Play:
```bash
# Basic run
java -jar ClawCTF_Challenge.jar

# Debug mode (gives hints)
java -jar ClawCTF_Challenge.jar debug

# Help/solution path
java -jar ClawCTF_Challenge.jar solve