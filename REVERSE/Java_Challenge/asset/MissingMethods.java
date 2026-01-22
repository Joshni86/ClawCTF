public class MissingMethods {
    public static void revealFlagPart1() {
        System.out.println("CTF{this_is_part1_");
    }
    
    public static String getPartA() {
        return "CTF{";
    }
    
    public static String getPartB() {
        return "java_";
    }
    
    public static String getPartC() {
        return "bytecode}";
    }
}