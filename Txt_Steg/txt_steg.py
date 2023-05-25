import numpy as np

class txt_steg:
    def __init__(self, text_file: str = "text.txt", bit_to_hide: list[int] = None):
        """
        Initialize the class
        :param text_file: PathName of the text file to encode or decode
        :type text_file: str
        :param bit_to_hide: Bit to hide the data in (1 - LSB to 8 - MSB)
        :type bit_to_hide: int
        """
        self.text_file = text_file
        self.bit_to_hide = [8 - bit_pos for bit_pos in bit_to_hide]
        self.delimiter = "abc-123=="

    def encode(self, secret_data: str = "Hello World"):
        """
        Encode the secret data into the text file
        :param secret_data: String
        :type secret_data: str
        """
        print("[+] Encoding...")
        # Read text file and covert to binary
        if self.text_file != "":
            with open(self.text_file, "r") as f:
                data = f.read()
        else:
            raise FileNotFoundError("File not found")

        secret_data += self.delimiter  # Add delimiter

        # Max Bytes to encode
        n_bytes = len(data) // 8

        # Check if secret data can be encoded into text file
        if len(secret_data) > n_bytes:
            raise ValueError(
                f"[-] Error: Binary Secret data length {len(secret_data)} is greater than data length {n_bytes}")

        bits_to_hide = self.bit_to_hide
        data_index = 0
        # Convert secret data to binary
        binary_secret_data = self.to_bin(secret_data)

        encoded_data = ""

        # Encode data into text file
        for byte in data:
            byte = self.to_bin(byte)
            byte = "0" * (8 - len(byte)) + byte
            if data_index >= len(binary_secret_data):
                encoded_data += byte
            else:
                for bit_pos in bits_to_hide:
                    if data_index < len(binary_secret_data):
                        byte = list(byte)
                        byte[bit_pos] = binary_secret_data[data_index]
                        data_index += 1
                encoded_data += self.from_bin(''.join(byte))

        return encoded_data

    def decode(self) -> str:
        """
        Decode the encoded data from the text file

        Secret text is stored in the bit_to_hide positions
        :return: Decoded Data: String
        """
        print("[+] Decoding...")
        # Read text file and covert to binary
        if self.text_file != "":
            with open(self.text_file, "r") as f:
                data = f.read()
        else:
            raise FileNotFoundError("File not found")

        binary_data = ""
        bit_to_hide = self.bit_to_hide

        for byte in data:
            byte = self.to_bin(byte)
            byte = "0" * (8 - len(byte)) + byte
            for bit_pos in bit_to_hide:
                binary_data += byte[bit_pos]

        all_bytes = [binary_data[i:i + 8] for i in range(0, len(binary_data), 8)]

        decoded_data = ""
        for byte in all_bytes:
            decoded_data += chr(int(byte, 2))
            if decoded_data[-len(self.delimiter):] == self.delimiter:
                break

        return decoded_data[:-len(self.delimiter)]

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

    def from_bin(self, data: str) -> str:
        """
        Convert binary `data` back to the original format
        :param data: String
        :type data: str
        :return: Original Data: String
        """

        return ''.join([chr(int(data[i:i + 8], 2)) for i in range(0, len(data), 8)])


def main():
    print("Welcome to Text Steganography")
    text_file_name = "test.txt"
    secret_data = "vulputate. In tincidunt arcu risus, eu lacinia metus viverra in. Maecenas id ipsum tortor. Nunc vita" \
                  " e mauris vel turpis lobortis tincidunt sed sit amet purus. Aliquam sed pharetra neque. Sed eget nis" \
                  "i id metus aliquam dapibus et nec felis. Cras quis ante rutrum, bibendum lacus ut, malesuada justo. "

    # Create a unique random number list from 1-8, spanning anywhere from 1-8 bits, for testing purposes
    bits_to_hide = np.random.choice(range(1, 9), np.random.randint(1, 9), replace=False)
    bits_to_hide = list(bits_to_hide)
    bits_to_hide.sort()
    print(f"Bits to hide: {bits_to_hide}")

    # Encode
    encoded_file_name = "encoded_text.txt"
    encoded_data = txt_steg(text_file_name, bits_to_hide).encode(secret_data)
    with open(f"{encoded_file_name}", "w") as f:
        f.write(encoded_data)

    # Decode
    decoded_data = txt_steg(encoded_file_name, bits_to_hide).decode()
    print(decoded_data)


if __name__ == "__main__":
    main()
