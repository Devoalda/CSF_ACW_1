import numpy as np


class txt_steg:
    def __init__(self, text_file: str = None, bit_to_hide: list[int] = None) -> None:
        """
        Initialize the class
        :param text_file: PathName of the text file to encode or decode (Required)
        :type text_file: str
        :param bit_to_hide: Bit to hide the data in (1 - LSB to 8 - MSB), Default is LSB (index = 7)
        :type bit_to_hide: list[int]
        """
        if text_file:
            self.text_file = text_file
        else:
            raise FileNotFoundError("Please specify a text file")
        self.bit_to_hide = [8 - bit_pos for bit_pos in bit_to_hide] if bit_to_hide else [7]
        self.delimiter = "abc-123=="  # Delimiter to indicate the end of the secret data

    def encode(self, secret_data: str = "Hello World") -> str:
        """
        Encode the secret data into the text file
        :param secret_data: String
        :type secret_data: str
        """
        # Read text file
        with open(self.text_file, "r") as f:
            data = f.read()

        secret_data += self.delimiter  # Add delimiter

        # Max Bits to encode (1 Character = 8 bits)
        n_bits = len(data) * len(
            self.bit_to_hide)  # Bits that can be used (Each character x Number of bits that can be used)

        # Check if secret data can be encoded into text file
        if len(secret_data) * 8 > n_bits:
            raise ValueError(
                f"[-] Error: Binary Secret data length {len(secret_data) * 8} is greater than data length {n_bits}")

        data_index = 0
        # Convert secret data to binary
        binary_secret_data = self.to_bin(secret_data)

        encoded_data = ""

        # Encode data into text
        for char in data:
            bin_char = self.to_bin(char)
            bin_char = "0" * (8 - len(bin_char)) + bin_char
            if data_index >= len(binary_secret_data):
                encoded_data += self.from_bin(''.join(bin_char))
            else:
                for bit_pos in self.bit_to_hide:
                    if data_index < len(binary_secret_data):
                        bin_char = list(bin_char)
                        bin_char[bit_pos] = binary_secret_data[data_index]
                        data_index += 1
                encoded_data += self.from_bin(''.join(bin_char))

        return encoded_data

    def decode(self) -> str:
        """
        Decode the encoded data from the text file

        Secret text is stored in the bit_to_hide positions
        :return: Decoded Data: String
        """
        # Read text file and covert to binary
        with open(self.text_file, "r") as f:
            data = f.read()

        binary_data = ""
        for char in data:
            bin_char = self.to_bin(char)
            bin_char = "0" * (8 - len(bin_char)) + bin_char
            for bit_pos in self.bit_to_hide:
                binary_data += bin_char[bit_pos]

        all_chars = [binary_data[i:i + 8] for i in range(0, len(binary_data), 8)]

        decoded_data = ""
        for char in all_chars:
            decoded_data += chr(int(char, 2))
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
    raise NotImplementedError("This module is not meant to run by itself")
    # print("Welcome to Text Steganography")
    # text_file_name = "test.txt"
    # with open("../Txt_Steg/secret_data.txt", "r") as f:
    #     secret_data = f.read()
    #
    # # Create a unique random number list from 1-8, spanning anywhere from 1-8 bits, for testing purposes
    # bits_to_hide = np.random.choice(range(1, 9), np.random.randint(1, 9), replace=False)
    # bits_to_hide = list(bits_to_hide)
    # bits_to_hide.sort()
    # print(f"Bits to hide: {bits_to_hide}")
    #
    # # Encode
    # encoded_file_name = "encoded_text.txt"
    # encoded_data = txt_steg(text_file=text_file_name, bit_to_hide=bits_to_hide).encode(secret_data)
    # with open(f"{encoded_file_name}", "w") as f:
    #     f.write(encoded_data)
    #
    # # Decode
    # decoded_data = txt_steg(text_file=encoded_file_name, bit_to_hide=bits_to_hide).decode()
    # print(decoded_data)


if __name__ == "__main__":
    main()
