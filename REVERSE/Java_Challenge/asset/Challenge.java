import java.util.Random;
import java.util.Base64;

public class Challenge {
    
    public static void main(String[] args) {
        System.out.println("=== Java Bytecode Challenge ===");
        System.out.println("Find the hidden flag!");
        System.out.println("");
        
        // Layer 1: Fake flag (decoy)
        String fakeFlag = fakeDecrypt("Q2xhd0NURntmYWtlX2ZsYWdfaGVyZX0=");
        System.out.println("Decoy flag (ignore this): " + fakeFlag);
        System.out.println("");
        
        // Layer 2: Real flag but obfuscated
        if (args.length > 0 && args[0].equals("debug")) {
            System.out.println("🔧 Debug mode activated!");
            System.out.println("");
            
            System.out.println("Flag part 1: ClawCTF{");
            System.out.print("Flag part 2: ");
            
            // Show encoded part
            String encoded = "amF2YV9ieXRlY29kZV8="; // "java_bytecode_" in Base64
            String decoded = new String(Base64.getDecoder().decode(encoded));
            System.out.println(decoded);
            
            // Show third part via RealDecryptor
            RealDecryptor.decrypt();
            
            System.out.println("");
            System.out.println("Hint: Try running FlagParts.assembleFlag()");
        } else {
            System.out.println("💡 Try running with 'debug' argument:");
            System.out.println("   java -jar Challenge.jar debug");
            System.out.println("");
            System.out.println("Or decompile this JAR to find the flag!");
        }
    }
    
    private static String fakeDecrypt(String input) {
        // Returns a fake flag
        try {
            return new String(Base64.getDecoder().decode(input));
        } catch (Exception e) {
            return "ClawCTF{fake_flag_not_found}";
        }
    }
}