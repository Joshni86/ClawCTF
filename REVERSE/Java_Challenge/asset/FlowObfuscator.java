import java.util.concurrent.*;

public class FlowObfuscator {
    
    public static void confusingPath() {
        // Complex switch statement with dead cases
        int x = 42;
        String result = "";
        
        switch (x) {
            case 1:
                result = "dead_code_1";
                break;
            case 2:
                result = "CTF{";
                // Fall through intentionally
            case 3:
                result += "partial";
                break;
            case 42:  // This case executes
                result = executeComplexLogic();
                break;
            default:
                result = "default_" + System.nanoTime();
        }
        
        if (x > 100) {  // Never true
            System.out.println("Flag: " + result);
        }
    }
    
    private static String executeComplexLogic() {
        // Fibonacci-based decoding
        int a = 1, b = 1;
        int[] fibSequence = new int[10];
        for (int i = 0; i < 10; i++) {
            fibSequence[i] = a;
            int temp = a + b;
            a = b;
            b = temp;
        }
        
        // Use Fibonacci numbers as XOR keys
        int[] encoded = {70, 85, 72, 33, 90, 17, 94, 25, 85, 32, 94, 25, 88, 15};
        StringBuilder sb = new StringBuilder();
        
        for (int i = 0; i < encoded.length; i++) {
            sb.append((char)(encoded[i] ^ fibSequence[i % fibSequence.length]));
        }
        
        return sb.toString();  // Returns: _control_flow_
    }
    
    // Async execution that never completes
    public static void asyncObfuscation() {
        ExecutorService executor = Executors.newSingleThreadExecutor();
        Future<String> future = executor.submit(() -> {
            Thread.sleep(10000);  // Never returns
            return "CTF{async_flag}";
        });
        
        executor.shutdown();
    }
}