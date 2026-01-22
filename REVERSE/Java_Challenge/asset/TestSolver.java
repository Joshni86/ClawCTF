public class TestSolver {
    public static void main(String[] args) {
        System.out.println("=== ClawCTF Java Challenge Solver ===");
        System.out.println("");
        
        System.out.println("Testing all components...");
        System.out.println("");
        
        // Test 1: FlagParts
        System.out.println("1. FlagParts.assembleFlag():");
        System.out.println("   Result: " + FlagParts.assembleFlag());
        System.out.println("");
        
        // Test 2: RealDecryptor
        System.out.println("2. RealDecryptor.decrypt():");
        System.out.print("   Result: ");
        RealDecryptor.decrypt();
        System.out.println("");
        
        // Test 3: Show expected flag directly
        System.out.println("3. Expected complete flag:");
        System.out.println("   ClawCTF{java_bytecode_control_flow_obfuscated}");
        System.out.println("");
        
        System.out.println("To get the flag directly, run:");
        System.out.println("   java -cp ClawCTF_Challenge.jar FinalFlag");
    }
}