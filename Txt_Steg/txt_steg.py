import numpy as np


class txt_steg:
    def __init__(self, text_file: str = "text.txt", bit_to_hide: int = 2):
        """
        Initialize the class
        :param text_file: PathName of the text file to encode or decode
        :type text_file: str
        :param bit_to_hide: Bit to hide the data in (1 - LSB to 8 - MSB)
        :type bit_to_hide: int
        """
        self.text_file = text_file
        self.bit_to_hide = 8 - bit_to_hide
        self.delimiter = "abc12345"

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
        binary_data = ''.join([c for c in data if c in ('0', '1')])  # Remove non-binary characters

        # Split the binary data into chunks of 8 bits
        binary_parts = [binary_data[i:i + 8] for i in range(0, len(binary_data), 8)]

        # Convert each chunk to its corresponding ASCII character
        decoded_data = ''.join([chr(int(part, 2)) for part in binary_parts])

        return decoded_data

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
            f.close()
            data = self.to_bin(data)
        else:
            raise FileNotFoundError("File not found")

        bits_to_hide = self.bit_to_hide

        secret_data += self.delimiter  # Add delimiter
        binary_secret_data = self.to_bin(secret_data)
        data_len = len(data)

        # Check if secret data can be encoded into text file
        if len(binary_secret_data) > data_len:
            raise ValueError(f"[-] Error: Binary Secret data length {len(binary_secret_data)} "
                             f"is greater than data length {data_len}")

        encoded_data = ""

        # For every 8 bits in the data, hide 1 bit of secret data in the bit_to_hide position
        data_index = 0
        for i in range(0, data_len, 8):
            data_byte = data[i:i + 8]
            if data_index < len(binary_secret_data):
                secret_bit = binary_secret_data[data_index]
                modified_byte = data_byte[:bits_to_hide] + secret_bit + data_byte[bits_to_hide + 1:]
                encoded_data += modified_byte
                data_index += 1
            else:
                encoded_data += data_byte

        encoded_data = self.from_bin(encoded_data)

        return encoded_data

    def decode(self) -> str:
        """
        Decode the encoded data from the text file
        :return: Decoded Data: String
        """
        print("[+] Decoding...")
        # Read text file and covert to binary
        if self.text_file != "":
            with open(self.text_file, "r") as f:
                data = f.read()
            f.close()
            data = self.to_bin(data)
        else:
            raise FileNotFoundError("File not found")

        # Split the data into bytes
        bytes_data = [data[i:i + 8] for i in range(0, len(data), 8)]

        # Extract the bits at the bit_to_hide position
        secret_data = [byte[self.bit_to_hide] for byte in bytes_data]

        # Concatenate the bits into a binary string
        binary_data = ''.join(secret_data)

        # Split the binary data using the delimiter
        delimeter_as_bin = self.to_bin(self.delimiter)
        binary_data = binary_data.split(delimeter_as_bin)[0]

        # Convert the binary data back to the original text
        decoded_data = self.from_bin(binary_data)

        return decoded_data


def main():
    print("Welcome to Text Steganography")
    print("1. Encode\n2. Decode\n3. Exit")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        text_file_name = input("Enter name of text file to encode: ")
        secret_data = input("Enter data to encode: ")
        bit_to_hide = int(input("Enter bit to hide (1 - LSB to 8 - MSB): "))
        encoded_data = txt_steg(text_file_name, bit_to_hide).encode(secret_data)
        extension = text_file_name.split(".")[-1]
        with open(f"encoded_text.{extension}", "w") as f:
            f.write(encoded_data)
        print("Encoded Data:", encoded_data)
    elif choice == 2:
        text_file_name = input("Enter name of text file to decode: ")
        bit_to_hide = int(input("Enter bit to hide (1 - LSB to 8 - MSB): "))
        decoded_data = txt_steg(text_file_name, bit_to_hide).decode()
        print("Decoded Data:", decoded_data)


if __name__ == "__main__":
    main()
