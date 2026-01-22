import java.lang.reflect.*;

public class FinalFlag {
    
    private static class InnerSecret {
        private String realFlag = "ClawCTF{java_bytecode_control_flow_obfuscated}";
        
        private String getRealFlag() {
            return realFlag;
        }
    }
    
    public static void main(String[] args) throws Exception {
        System.out.println("=== Secret Flag Revealer ===");
        System.out.println("(This class reveals the complete flag)");
        System.out.println("");
        
        InnerSecret secret = new InnerSecret();
        Class<?> clazz = secret.getClass();
        
        Field field = clazz.getDeclaredField("realFlag");
        field.setAccessible(true);
        
        String flag = (String) field.get(secret);
        System.out.println("🎯 The complete flag is: " + flag);
        System.out.println("");
        System.out.println("Flag breakdown:");
        System.out.println("  Prefix: ClawCTF{");
        System.out.println("  Content: java_bytecode_control_flow_obfuscated");
        System.out.println("  Suffix: }");
    }
}