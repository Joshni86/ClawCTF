public class RealDecryptor {
    // Encrypted: "_control_flow_obfuscated}" XOR with 0x15
    // Note: The "ClawCTF{java_bytecode" part is elsewhere
    private static final byte[] ENCRYPTED = {
        (byte)(95^0x15),   // '_'
        (byte)(99^0x15),   // 'c'
        (byte)(111^0x15),  // 'o'
        (byte)(110^0x15),  // 'n'
        (byte)(116^0x15),  // 't'
        (byte)(114^0x15),  // 'r'
        (byte)(111^0x15),  // 'o'
        (byte)(108^0x15),  // 'l'
        (byte)(95^0x15),   // '_'
        (byte)(102^0x15),  // 'f'
        (byte)(108^0x15),  // 'l'
        (byte)(111^0x15),  // 'o'
        (byte)(119^0x15),  // 'w'
        (byte)(95^0x15),   // '_'
        (byte)(111^0x15),  // 'o'
        (byte)(98^0x15),   // 'b'
        (byte)(102^0x15),  // 'f'
        (byte)(117^0x15),  // 'u'
        (byte)(115^0x15),  // 's'
        (byte)(99^0x15),   // 'c'
        (byte)(97^0x15),   // 'a'
        (byte)(116^0x15),  // 't'
        (byte)(101^0x15),  // 'e'
        (byte)(100^0x15),  // 'd'
        (byte)(125^0x15)   // '}'
    };
    
    private static final int KEY = 0x15;
    
    public static void decrypt() {
        System.out.print("Flag part 3: ");
        for (byte b : ENCRYPTED) {
            System.out.print((char)(b ^ KEY));
        }
        System.out.println();
    }
}