import struct
import time
import secrets

# --- VM Opcode Definitions ---
# Using random-ish high values to make manual analysis slightly annoying without the definition
OP_NOP      = 0x10
OP_LOAD     = 0x1A  # Load immediate (u32) to stack
OP_LOAD_REG = 0x1B  # Load register to stack. Arg: reg_idx
OP_STORE_REG= 0x1C  # Pop stack to register. Arg: reg_idx
OP_ADD      = 0x20  # Pop a, pop b, push a + b
OP_SUB      = 0x21  # Pop a, pop b, push a - b
OP_XOR      = 0x22  # Pop a, pop b, push a ^ b
OP_MUL      = 0x23  # Pop a, pop b, push a * b
OP_JMP      = 0x30  # Unconditional relative jump. Arg: offset (i16)
OP_JZ       = 0x31  # Pop val. If 0, jump relative. Arg: offset (i16)
OP_JNZ      = 0x32  # Pop val. If != 0, jump relative. Arg: offset (i16)
OP_TIME     = 0x40  # Push current timestamp (simulated or real)
OP_EXIT     = 0xFF  # Terminate VM

# Registers
REG_ACC     = 0
REG_MAINT   = 1 # "Maintenance Mode" register (secretly used)
REG_FLAGS   = 2 # 1=Expired, 2=Valid, 4=Magic
REG_TEMP    = 3

# Flags
FLAG_EXPIRED = 1
FLAG_VALID   = 2
FLAG_MAGIC   = 4

class BytecodeBuilder:
    def __init__(self):
        self.code = bytearray()
        self.labels = {} # name -> byte_offset
        self.jumps = []  # (offset_in_code, label_name)

    def emit(self, opcode):
        self.code.append(opcode)

    def emit_u8(self, val):
        self.code.append(val & 0xFF)

    def emit_i16(self, val):
        self.code.extend(struct.pack('<h', val))

    def emit_u32(self, val):
        self.code.extend(struct.pack('<I', val))

    def label(self, name):
        self.labels[name] = len(self.code)

    def jump(self, opcode, label_name):
        self.emit(opcode)
        self.jumps.append((len(self.code), label_name))
        self.emit_i16(0) # Placeholder

    # Helpers
    def load(self, val):
        self.emit(OP_LOAD)
        self.emit_u32(val)

    def load_reg(self, reg):
        self.emit(OP_LOAD_REG)
        self.emit_u8(reg)
    
    def store_reg(self, reg):
        self.emit(OP_STORE_REG)
        self.emit_u8(reg)

    def op(self, opcode):
        self.emit(opcode)

    def finalize(self):
        # Patch jumps
        for patch_offset, label_name in self.jumps:
            if label_name not in self.labels:
                raise ValueError(f"Undefined label: {label_name}")
            target = self.labels[label_name]
            # Calculate relative offset
            # Jump offset is relative to the start of the NEXT instruction? 
            # Or usually relative to the current IP. Let's say relative to NEXT instruction start (after the i16 operand).
            # The operand is at patch_offset. The next instruction starts at patch_offset + 2.
            # So dist = target - (patch_offset + 2)
            dist = target - (patch_offset + 2)
            struct.pack_into('<h', self.code, patch_offset, dist)
        return self.code

def build_challenge_logic():
    b = BytecodeBuilder()
    
    # 0. HEADER MAGIC (Hint)
    # Just putting some NOPs or distinct values that spell something in hex?
    # Or just functional logic. Let's do functional.
    
    # --- Hint strings data chunk (loaded but not executed directly, placed at start maybe?) ---
    # Actually, let's keep it pure code for now to avoid complexity of data segment registers.
    
    # 1. Initialize logic
    b.load(0) 
    b.store_reg(REG_FLAGS) # Clear flags
    
    # 2. Fake "Complexity" (Noise)
    # Calculate some nonsense: ((0x1337 ^ 0xDEAD) + 5) * 2
    b.load(0x1337)
    b.load(0xDEAD)
    b.op(OP_XOR)
    b.load(5)
    b.op(OP_ADD)
    b.load(2)
    b.op(OP_MUL)
    b.store_reg(REG_ACC) # Store result in ACC (ignored)

    # 3. Time Check
    b.op(OP_TIME)          # Push current time
    b.load(1735689600)     # 2025-01-01 00:00:00 (Basically already passed)
    b.op(OP_SUB)           # time - expiry
    # If time > expiry, result is positive (or non-zero). 
    # Let's simplify: if (time - expiry) > 0, we are expired.
    # Actually, let's just use subtraction. If result is positive (high bit 0), it's future.
    # Wait, simple subtraction logic with limited opcodes.
    # Let's just check if (time > expiry).
    # Since I don't have GT/LT, let's assume TIME returns a small integer for "is_expired" for simplicity in this custom VM?
    # No, better: OP_TIME pushes Unix timestamp.
    # Let's assume we are definitely expired.
    # (time - expiry) will be positive large number.
    # Let's simple check:
    #   Load Expiry
    #   Load Time
    #   SUB
    #   If result has high bit set (negative), then Time < Expiry (Not Expired).
    #   If result has high bit clear (positive), then Time >= Expiry (Expired).
    #   This presumes 32-bit math.
    
    # Let's make it deterministic. The VM logic will ALWAYS act as if expired because the hardcoded date is old.
    
    # Real logic:
    b.label("check_expiry")
    b.load(1)               # EXPIRY_FLAG_BIT
    b.store_reg(REG_FLAGS)  # Set Expired immediately. (Pessimistic approach)
                            # Now player sees FLAG=1 (Expired)
    
    # 4. The "Maintenance Mode" Check (Hidden Path)
    # We check if REG_MAINT contains a specific magic value.
    # This value must be supplied by the native code based on some input or patched by the user.
    # Wait, the native code needs to set this?
    # Or maybe the bytecode checks a "secret input" provided via stack?
    # Let's say we check REG_MAINT. The default is 0. 
    # If the user finds this, they realize they need to set REG_MAINT to 0x1337BEEF somehow.
    # How? The challenge says "The VM must support at least one valid execution path...".
    # Maybe we derive REG_MAINT from the input key?
    # Let's say the native code parses the key, puts part of it into REG_MAINT before starting VM.
    # If the key has a special suffix or prefix, REG_MAINT gets set.
    # But native code is "fake".
    # Ok, let's make it simpler: The instruction stream checks a specific memory address or register
    # that is populated by the 'native_check' IF the key has a certain pattern.
    # Since we want the native check to be 'fake' but also 'misleading', maybe the native check
    # DOES parse the key correctly but returns 'success' which is ignored.
    # HOWEVER, a side effect of the native check is setting a global variable that the VM reads via 'OP_LOAD_REG' or similar.
    
    # Better: The VM bytecode performs a check on values pushed to the stack at startup.
    # The native code pushes arguments: [KeyPart1, KeyPart2]
    # KeyPart1 is standard serial (fake check verifies this).
    # KeyPart2 is usually 0.
    # But if KeyPart2 is the magic "Maintenance Code", we bypass expiry.
    
    b.load_reg(REG_MAINT)       # Check Maintenance Register
    b.load(0xC0DEFEFE)          # Magic Maintenance Key
    b.op(OP_XOR)
    b.jump(OP_JZ, "valid_override") # If (REG_MAINT ^ MAGIC) == 0, Jump to Valid
    
    # Normal Path (Expired)
    b.jump(OP_JMP, "fail")

    b.label("valid_override")
    # 5. Success State
    # Need to set Valid and Magic flags.
    b.load_reg(REG_FLAGS)
    b.load(FLAG_VALID | FLAG_MAGIC) # 2 | 4 = 6. Result is 1 | 6 = 7.
    b.op(OP_ADD) # (Existing 1) + 6 = 7. (Expired + Valid + Magic)
    b.store_reg(REG_FLAGS)
    
    # Hint: "Maintenance Active" - maybe implicit by reaching here.
    b.jump(OP_JMP, "exit")

    b.label("fail")
    # Failed state. Just exit with whatever flags (Default is 1=Expired)
    # Or maybe set a specific error code in ACC
    b.load(0xDEAD)
    b.store_reg(REG_ACC)
    
    b.label("exit")
    b.op(OP_EXIT)
    
    return b.finalize()

def encrypt_bytecode(data):
    # Rolling XOR key
    key = 0xAA
    encrypted = bytearray()
    for b in data:
        encrypted.append(b ^ key)
        key = (key + 1) & 0xFF
    return encrypted

def generate_header(encrypted_data):
    # Output C++ compatible array
    output = "const unsigned char vm_bytecode[] = {\n    "
    for i, b in enumerate(encrypted_data):
        output += f"0x{b:02x}, "
        if (i + 1) % 12 == 0:
            output += "\n    "
    output += "\n};\n"
    output += f"const size_t vm_bytecode_len = {len(encrypted_data)};"
    return output

if __name__ == "__main__":
    raw_code = build_challenge_logic()
    enc_code = encrypt_bytecode(raw_code)
    header_content = generate_header(enc_code)
    
    # Also generate the OPCODE definitions for C++
    cpp_header = """
#pragma once
#include <cstdint>
#include <vector>

// Opcode Definitions
enum VMOpcode : uint8_t {
    OP_NOP      = 0x10,
    OP_LOAD     = 0x1A,
    OP_LOAD_REG = 0x1B,
    OP_STORE_REG= 0x1C,
    OP_ADD      = 0x20,
    OP_SUB      = 0x21,
    OP_XOR      = 0x22,
    OP_MUL      = 0x23,
    OP_JMP      = 0x30,
    OP_JZ       = 0x31,
    OP_JNZ      = 0x32,
    OP_TIME     = 0x40,
    OP_EXIT     = 0xFF
};

// Flags
const uint32_t FLAG_EXPIRED = 1;
const uint32_t FLAG_VALID   = 2;
const uint32_t FLAG_MAGIC   = 4;

// Registers
const int REG_ACC     = 0;
const int REG_MAINT   = 1;
const int REG_FLAGS   = 2;
const int REG_TEMP    = 3;
const int NUM_REGS    = 4;

"""
    cpp_header += header_content
    
    with open("vm_data.h", "w") as f:
        f.write(cpp_header)
    
    print("Generated vm_data.h with bytecode length:", len(enc_code))
