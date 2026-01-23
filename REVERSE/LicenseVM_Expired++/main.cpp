#include <iostream>
#include <vector>
#include <string>
#include <ctime>
#include <cstring>
#include <iomanip>
#include "vm_data.h"

// --- Fake Legacy Check (Misdirection) ---
// This function looks like a standard serial validator.
// It returns true/false but is largely ignored by the critical path.
bool verify_license_legacy_v1(const std::string& key) {
    // Expected format: AAAA-BBBB-CCCC-DDDD
    if (key.length() != 19) return false;
    if (key[4] != '-' || key[9] != '-' || key[14] != '-') return false;
    
    int score = 0;
    for (char c : key) {
        if (isalnum(c)) score += c;
    }
    
    // Fake checksum logic
    if (score % 7 == 0) {
        // "Debug" message that suggests this might be important
        // Using volatile to prevent optimization
        volatile int x = 10;
        (void)x; 
        return true;
    }
    return false;
}

// --- VM Context ---
struct VMContext {
    uint32_t stack[256];
    uint8_t sp = 0;
    uint32_t regs[NUM_REGS];
    bool running = true;
};

// --- VM Interpreter ---
void run_vm(VMContext& ctx, const uint8_t* encrypted_bytecode, size_t len) {
    // Decrypt bytecode in memory
    std::vector<uint8_t> code(len);
    uint8_t key = 0xAA;
    for (size_t i = 0; i < len; ++i) {
        code[i] = encrypted_bytecode[i] ^ key;
        key = (key + 1) & 0xFF; // Rolling key match
    }

    size_t ip = 0;
    
    // Hint: Print something about initializing engine
    // std::cout << "[*] Initializing core verification engine (VM_T3)..." << std::endl; 
    // Maybe too verbose for a "silent" CLI tool? Let's leave it out or make it part of verbose mode if there was one.
    // The plan suggested hint strings. Let's put one in the binary but not print it directly unless triggered?
    const char* hint_str = "Maintenance mode inactive."; 
    volatile const char* _touch = hint_str; (void)_touch;

    while (ctx.running && ip < len) {
        uint8_t opcode = code[ip++];
        
        switch (opcode) {
            case OP_NOP:
                break;
            case OP_LOAD: {
                // assume u32 follows
                if (ip + 4 > len) { ctx.running = false; break; }
                uint32_t val = 0;
                // Little endian load
                val |= code[ip+0] << 0;
                val |= code[ip+1] << 8;
                val |= code[ip+2] << 16;
                val |= code[ip+3] << 24;
                ip += 4;
                ctx.stack[ctx.sp++] = val;
                break;
            }
            case OP_LOAD_REG: {
                uint8_t reg = code[ip++];
                if (reg < NUM_REGS)
                    ctx.stack[ctx.sp++] = ctx.regs[reg];
                break;
            }
            case OP_STORE_REG: {
                uint8_t reg = code[ip++];
                if (ctx.sp > 0 && reg < NUM_REGS)
                    ctx.regs[reg] = ctx.stack[--ctx.sp];
                break;
            }
            case OP_ADD: {
                if (ctx.sp >= 2) {
                    uint32_t b = ctx.stack[--ctx.sp];
                    uint32_t a = ctx.stack[--ctx.sp];
                    ctx.stack[ctx.sp++] = a + b;
                }
                break;
            }
            case OP_SUB: {
                if (ctx.sp >= 2) {
                    uint32_t b = ctx.stack[--ctx.sp];
                    uint32_t a = ctx.stack[--ctx.sp];
                    ctx.stack[ctx.sp++] = a - b;
                }
                break;
            }
            case OP_XOR: {
                if (ctx.sp >= 2) {
                    uint32_t b = ctx.stack[--ctx.sp];
                    uint32_t a = ctx.stack[--ctx.sp];
                    ctx.stack[ctx.sp++] = a ^ b;
                }
                break;
            }
            case OP_MUL: {
                if (ctx.sp >= 2) {
                    uint32_t b = ctx.stack[--ctx.sp];
                    uint32_t a = ctx.stack[--ctx.sp];
                    ctx.stack[ctx.sp++] = a * b;
                }
                break;
            }
            case OP_JMP: {
                int16_t off = 0;
                off |= code[ip+0] << 0;
                off |= code[ip+1] << 8;
                ip += 2;
                ip += off; // Relative jump
                break;
            }
            case OP_JZ: {
                int16_t off = 0;
                off |= code[ip+0] << 0;
                off |= code[ip+1] << 8;
                ip += 2;
                if (ctx.sp > 0) {
                    uint32_t val = ctx.stack[--ctx.sp];
                    if (val == 0) ip += off;
                }
                break;
            }
            case OP_JNZ: {
                int16_t off = 0;
                off |= code[ip+0] << 0;
                off |= code[ip+1] << 8;
                ip += 2;
                if (ctx.sp > 0) {
                    uint32_t val = ctx.stack[--ctx.sp];
                    if (val != 0) ip += off;
                }
                break;
            }
            case OP_TIME: {
                // Hardcoded time logic in VM
                // Push current time as unix timestamp (32-bit)
                // For determinism in challenge, we can just call time(0)
                uint32_t t = (uint32_t)time(0);
                ctx.stack[ctx.sp++] = t;
                break;
            }
            case OP_EXIT: {
                ctx.running = false;
                break;
            }
            default:
                // Unknown opcode - crash or stop
                ctx.running = false;
                break;
        }
    }
}

// --- Main Challenge Logic ---
int main() {
    std::cout << "===========================================" << std::endl;
    std::cout << "   ProLicense Manager v3.0 (Enterprise)    " << std::endl;
    std::cout << "===========================================" << std::endl;
    
    std::string key;
    std::cout << "Enter License Key: ";
    std::cin >> key;

    // 1. Run Fake/Legacy Check
    // "Legacy" hints that this isn't the real check
    if (verify_license_legacy_v1(key)) {
        // Does nothing useful, just prints valid but continues
        // The user might think they won, but then the next part fails.
        // std::cout << "Legacy validation: OK" << std::endl; // Too obvious?
    } else {
        // std::cout << "Legacy validation: FAIL" << std::endl;
    }

    // Prepare VM
    VMContext ctx;
    memset(ctx.regs, 0, sizeof(ctx.regs));
    
    // SECRET: If the key contains "ADMIN" or specific pattern, set MAINT register
    // The "Magic Value" in generator.py is 0xC0DEFEFE.
    // Let's hide this injection.
    // Simple XOR check on input string:
    // If the user inputs a key that causes a certain hash, we set the register.
    // Or simpler: Look for a suffix.
    // Let's say: "XXXX-XXXX-XXXX-XXXX--MAINT" 
    // Or maybe just if the input *starts* with a specific magic sequence?
    // Let's try parsing the key for the magic integer directly.
    // No, that's too guessing.
    // Let's say: The user has to provide a second argument? No, single executable.
    
    // Implementing "Magic Pattern" in the key string:
    // If key contains "#MAINT#", calculate the magic.
    // Or simpler: The "secret" is part of the challenge. The user sees `OP_LOAD_REG REG_MAINT` in the VM.
    // They trace back to main to see where REG_MAINT comes from.
    // They see this block:
    if (key.length() > 5 && key.substr(0, 5) == "MAGIC") {
         // This is too obvious?
         // Let's make it a bit arithmetic.
         // Sum of chars should be X?
         // No, let's use the MAGIC value directly as an integer conversion?
         // "3235839742" is 0xC0DEFEFE in decimal.
         // If input == "3235839742", set reg.
         // But that's not a license key format.
         
         // Let's stick to the "suffix" idea but obfuscate the string check.
         const char* suffix = "++AUTH"; // Matches "ClawCTF{...++}" theme
         if (key.find(suffix) != std::string::npos) {
             ctx.regs[REG_MAINT] = 0xC0DEFEFE;
         }
    }
    
    // Run VM
    run_vm(ctx, vm_bytecode, vm_bytecode_len);
    
    // Check results
    uint32_t flags = ctx.regs[REG_FLAGS];
    
    bool expired = (flags & FLAG_EXPIRED);
    bool valid   = (flags & FLAG_VALID);
    bool magic   = (flags & FLAG_MAGIC);
    
    if (valid && magic) {
        // SUCCESS PATH
        // Construct the flag
        // ClawCTF{L1censeVM_Exp1red++}
        char flag[] = "ClawCTF{L1censeVM_Exp1red++}";
        std::cout << "\n[+] License Verified via Enhanced Protocol." << std::endl;
        std::cout << "[+] Feature Set Unlocked: FULL" << std::endl;
        std::cout << "[+] Flag: " << flag << std::endl;
        return 0;
    } else if (expired) {
        std::cout << "\n[-] License Expired. (Code: 0x1)" << std::endl;
        std::cout << "[-] Please contact support to renew your subscription." << std::endl;
        return 1;
    } else {
        std::cout << "\n[-] Invalid License. (Code: 0x0)" << std::endl; // Shouldn't happen given logic
        return 1;
    }
}
