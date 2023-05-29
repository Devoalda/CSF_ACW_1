import numpy as np


class mp3_steg:
    def __init__(self, mp3_file: str = "audio.mp3", bits_to_hide: list[int] = None):
        """
        Initialize the class
        :param mp3_file: PathName of the mp3 file to encode or decode
        :type mp3_file: str
        :param bits_to_hide: Bit to hide the data in (1 - LSB to 8 - MSB)
        :type bits_to_hide: list[int]
        """
        self.mp3_file = mp3_file
        self.bits_to_hide = [8 - bit_pos for bit_pos in bits_to_hide] if bits_to_hide else [1]  # Default is LSB
        self.delimiter = "12345"  # Delimiter to indicate the end of the secret data

    def encode(self, secret_data: str = "Hello World"):
        # Use struct to convert mp3 file to binary
        with open(self.mp3_file, "rb") as f:
            data = f.read()

        # Max Bytes to encode
        n_bytes = len(data) // 8

        # Check if secret data can be encoded into mp3 file
        print(f"Secret data length: {len(secret_data)}, Max data length: {n_bytes}")
        if len(secret_data) > n_bytes:
            raise ValueError(
                f"[-] Error: Binary Secret data length {len(secret_data)} is greater than data length {n_bytes}")

        # Convert secret data to binary
        binary_secret_data = self.to_bin(secret_data)

        # Add delimiter
        binary_secret_data += self.to_bin(self.delimiter)

        data_index = 0
        encoded_data = bytearray()

        print(f"[+] Starting encoding...")
        # Encode data into mp3
        for byte in data:
            if data_index >= len(binary_secret_data):
                encoded_data.append(byte)
            else:
                for bit_pos in self.bits_to_hide:
                    if data_index < len(binary_secret_data):
                        # Convert byte from int to binary string
                        byte = format(byte, "08b")
                        byte = list(byte)
                        byte[bit_pos] = binary_secret_data[data_index]
                        data_index += 1
                encoded_data.append(int(''.join(byte), 2))

        # Return encoded data as bytes
        return bytes(encoded_data)

    def decode(self):
        # Use struct to convert mp3 file to binary
        with open(self.mp3_file, "rb") as f:
            data = f.read()

        binary_data = ""
        print(f"[+] Starting decoding...")
        for byte in data:
            # Add byte to binary data
            # Convert byte from int to binary string
            byte = format(byte, "08b")
            # Pad byte with 0's to make sure it has 8 bits
            byte = "0" * (8 - len(byte)) + byte
            for bit_pos in self.bits_to_hide:
                binary_data += byte[bit_pos]

        all_bytes = [binary_data[i: i + 8] for i in range(0, len(binary_data), 8)]

        decoded_data = ""
        for byte in all_bytes:
            decoded_data += chr(int(byte, 2))
            # print(decoded_data)
            if decoded_data[-len(self.delimiter):] == self.delimiter:
                break

        # Return the decoded data
        return decoded_data

    def to_bin(self, data: str) -> str | list[str]:

        """
        Convert text file data to binary format as string
        :param data: String
        :type data: str
        :return: Binary Data: String | List[String]
        """
        if isinstance(data, str):
            return ''.join([format(ord(i), "08b") for i in data])
        elif isinstance(data, bytes) or isinstance(data, np.ndarray):
            return [format(i, "08b") for i in data]
        elif isinstance(data, int) or isinstance(data, np.unit8):
            return format(data, "08b")
        else:
            raise TypeError("Type not supported")


if __name__ == "__main__":

    with open("../Txt_Steg/secret_data.txt", "r") as f:
        secret_data = f.read()

    # Encode data into mp3 file
    mp3_steg_encode = mp3_steg(mp3_file="audio.mp3", bits_to_hide=[1])
    encoded_data = mp3_steg_encode.encode(secret_data="Hello")

    # Write encoded data to file
    with open("encoded_audio.mp3", "wb") as f:
        f.write(encoded_data)

    # Decode data from mp3 file
    steg_decode = mp3_steg(mp3_file="encoded_audio.mp3", bits_to_hide=[1])
    decoded_data = steg_decode.decode()

    # Print the decoded data
    print("[+] Decoded data:", decoded_data)
