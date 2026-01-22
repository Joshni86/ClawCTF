import java.util.Base64;

public class FlagParts {
    
    public static String CLAW() {
        return "ClawCTF{";
    }
    
    public static String part_java() {
        // "java_" but Caesar cipher (+1)
        return "sm`z_";  // Actually "java_" with each char + 1
    }
    
    public static String part_bytecode() {
        // "bytecode_" in Base64
        return "Ynl0ZWNvZGVf";
    }
    
    public static String part_obfuscated() {
        // "_control_flow" but XOR with 0x10
        byte[] bytes = {
            0x5F^0x10, 0x43^0x10, 0x4F^0x10, 0x4E^0x10, 0x54^0x10,
            0x52^0x10, 0x4F^0x10, 0x4C^0x10, 0x5F^0x10, 0x46^0x10,
            0x4C^0x10, 0x4F^0x10, 0x57^0x10
        };
        StringBuilder sb = new StringBuilder();
        for (byte b : bytes) {
            sb.append((char)b);
        }
        return sb.toString();
    }
    
    public static String assembleFlag() {
        // Decode part_java (Caesar -1)
        StringBuilder decodedJava = new StringBuilder();
        for (char c : part_java().toCharArray()) {
            decodedJava.append((char)(c - 1));
        }
        
        // Decode part_bytecode (Base64)
        String decodedBytecode = new String(Base64.getDecoder().decode(part_bytecode()));
        
        // Decode part_obfuscated (XOR with 0x10)
        StringBuilder decodedObfuscated = new StringBuilder();
        for (char c : part_obfuscated().toCharArray()) {
            decodedObfuscated.append((char)(c ^ 0x10));
        }
        
        return CLAW() + decodedJava.toString() + decodedBytecode + decodedObfuscated.toString();
    }
}