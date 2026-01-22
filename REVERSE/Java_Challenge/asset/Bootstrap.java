public class Bootstrap {
    public static void main(String[] args) {
        System.out.println("╔══════════════════════════════════════╗");
        System.out.println("║     Java Bytecode CTF Challenge      ║");
        System.out.println("║       Find the Hidden Flag!          ║");
        System.out.println("╚══════════════════════════════════════╝");
        System.out.println("");
        
        if (args.length == 0) {
            Challenge.main(new String[]{});
        } else if (args[0].equals("debug")) {
            Challenge.main(new String[]{"debug"});
        } else if (args[0].equals("solve")) {
            System.out.println("=== Solution Path ===");
            System.out.println("");
            System.out.println("1. Decompile the JAR file:");
            System.out.println("   Use JD-GUI, CFR, or javap");
            System.out.println("");
            System.out.println("2. Look at FlagParts.class:");
            System.out.println("   - The assembleFlag() method shows how to build it");
            System.out.println("   - Different encodings are used");
            System.out.println("");
            System.out.println("3. Check RealDecryptor.class:");
            System.out.println("   - Uses XOR with key 0x15");
            System.out.println("   - Contains part of the flag");
            System.out.println("");
            System.out.println("4. Or just run:");
            System.out.println("   java -cp Challenge.jar FinalFlag");
        } else {
            Challenge.main(args);
        }
    }
}