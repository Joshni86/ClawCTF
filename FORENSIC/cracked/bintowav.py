def binary_txt_to_wav(input_file, output_wav):
    # 1. Read the binary string from the text file
    with open(input_file, "r") as f:
        # Remove whitespace, newlines, or tabs
        binary_data = f.read().strip().replace(" ", "").replace("\n", "")

    # 2. Truncate to a multiple of 8 (ignore trailing bits that don't make a full byte)
    binary_data = binary_data[:len(binary_data) - len(binary_data) % 8]

    # 3. Convert binary string to raw bytes
    byte_array = bytearray()
    for i in range(0, len(binary_data), 8):
        byte_segment = binary_data[i:i+8]
        byte_array.append(int(byte_segment, 2))

    # 4. Save as .wav file
    # This writes the raw bytes directly. If the binary data includes the 
    # WAV header (RIFF...), this file will be playable immediately.
    with open(output_wav, "wb") as out:
        out.write(byte_array)

    print(f"✅ Audio written to: {output_wav}")

# Run the script
binary_txt_to_wav("binary.txt", "output.wav")