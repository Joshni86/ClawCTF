def wav_to_binary(input_wav, output_txt):
    try:
        # 1. Read the wav file as raw bytes
        with open(input_wav, "rb") as wav_file:
            raw_bytes = wav_file.read()

        # 2. Convert each byte into an 8-bit binary string
        # format(byte, '08b') ensures it stays 8 bits long (adds leading zeros)
        binary_string = "".join(format(byte, '08b') for byte in raw_bytes)

        # 3. Save the string of 0s and 1s to a text file
        with open(output_txt, "w") as f:
            f.write(binary_string)

        print(f"✅ Binary data written to: {output_txt}")
        print(f"Total bits: {len(binary_string)}")
        print(f"Total bytes processed: {len(raw_bytes)}")

    except FileNotFoundError:
        print(f"❌ Error: {input_wav} not found.")

# Run the function
wav_to_binary("rest.wav", "binary.txt")