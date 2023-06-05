import numpy as np


class file_steg:
    def __init__(self, file: str = None, bit_positions: list[int] = None) -> None:
        """
        Initialize the class
        :param file: Path to the file to encode or decode
        :type file: str
        :param bit_positions: Bit to hide the data in (1 - LSB to 8 - MSB) Default is LSB (index = 7)
        :type bit_positions: list[int]
        """
        self.supported_extensions = [
            "mp3",
            "mp4",
            "docx",
            "xlsx",
            "csv",
            "pptx",
            "jpg",
            "jpeg",
            "gif",
            "pdf"
        ]
        if file is None:
            raise ValueError(f"[-] Error: File path is required")
        if file.split(".")[-1] not in self.supported_extensions:
            raise ValueError(f"[-] Error: File extension {file.split('.')[-1]} is not supported")
        else:
            self.file = file

        self.bits_to_hide = [8 - bit_pos for bit_pos in bit_positions] if bit_positions else [7]  # Default is LSB
        self.delimiter = "LZu30,#"  # Delimiter to indicate the end of the secret data

    def encode(self, secret_data_str: str = "Hello World") -> bytes:
        """
        Encode the secret data into the mp3 file

        :param secret_data_str: String of data to hide

        :return: Encoded mp3 file as bytes
        :rtype: bytes
        """

        with open(self.file, "rb") as f:
            data = f.read()

        # Max Bytes to encode
        n_bytes = len(data) * 8 * len(self.bits_to_hide)

        if len(secret_data_str) * 8 > n_bytes:
            raise ValueError(
                f"[-] Error: Binary Secret data length {len(secret_data_str)} is greater than data length {n_bytes}")

        # Convert secret data to binary
        binary_secret_data = self.to_bin(secret_data_str)

        # Add delimiter
        binary_secret_data += self.to_bin(self.delimiter)

        data_index = 0
        encoded_data = bytearray()

        for byte in data:
            if data_index >= len(binary_secret_data):
                encoded_data.append(byte)
            else:
                for bit_pos in self.bits_to_hide:
                    if data_index < len(binary_secret_data):
                        byte = list(format(byte, "08b"))
                        byte = list(byte)
                        byte[bit_pos] = binary_secret_data[data_index]
                        data_index += 1
                        # Convert byte back to int
                        byte = int("".join(byte), 2)
                encoded_data.append(byte)

        return bytes(encoded_data)

    def decode(self) -> str:
        """
        Decode the secret data from the mp3 file
        :return: Decoded secret data
        :rtype: str
        """
        with open(self.file, "rb") as f:
            data = f.read()

        binary_data = ""
        decoded_data = ""
        for byte in data:
            # Add byte to binary data
            # Convert byte from int to binary string
            byte = format(byte, "08b")
            # Pad byte with 0's to make sure it has 8 bits
            byte = "0" * (8 - len(byte)) + byte
            for bit_pos in self.bits_to_hide:
                binary_data += byte[bit_pos]

        all_bytes = [binary_data[i: i + 8] for i in range(0, len(binary_data), 8)]

        for byte in all_bytes:
            decoded_data += chr(int(byte, 2))
            if decoded_data[-len(self.delimiter):] == self.delimiter:
                break

        # Return the decoded data
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


def main():
    raise NotImplementedError("This module is not meant to run by itself")


if __name__ == "__main__":
    main()
