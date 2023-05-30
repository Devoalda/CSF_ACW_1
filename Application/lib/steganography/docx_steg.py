import numpy as np

##################################################
# Duplicate of file_steg.py, to remove           #
##################################################
class docx_steg:
    def __init__(self, docx_file: str = "testfile.docx", bits_to_hide: list[int] = None) -> None:
        """
        Initialize the class
        :param docx_file: PathName of the docx file to encode or decode
        :type docx_file: str
        :param bits_to_hide: Bit to hide the data in (1 - LSB to 8 - MSB)
        :type bits_to_hide: list[int]
        """
        raise NotImplementedError("Duplicate of file_steg.py, to remove")
        self.docx_file = docx_file
        self.bits_to_hide = [8 - bit_pos for bit_pos in bits_to_hide] if bits_to_hide else [1]  # Default is LSB
        self.delimiter = "====="  # Delimiter to indicate the end of the secret data

    def encode(self, secret_data: str = "Hello World") -> bytes:
        """
        Encode the secret data into the docx file

        :param secret_data: String of data to hide

        :return: Encoded docx file as bytes
        :rtype: bytes
        """

        with open(self.docx_file, "rb") as f:
            data = f.read()

        # Max Bytes to encode
        n_bytes = len(data) // 8

        # Check if secret data can be encoded into docx file
        # print(f"Secret data length: {len(secret_data)}, Max data length: {n_bytes}")
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
        # Encode data into docx
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

        print(f"[+] Encoding completed successfully.")
        return bytes(encoded_data)

    def decode(self) -> str:
        """
        Decode the secret data from the docx file
        :return: Decoded secret data
        :rtype: str
        """
        with open(self.docx_file, "rb") as f:
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
            if decoded_data[-len(self.delimiter):] == self.delimiter:
                break

        print(f"[+] Decoding completed successfully.")
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

    def from_bin(self, data: str) -> str:
        """
        Convert binary `data` back to the original format
        :param data: String
        :type data: str
        :return: Original Data: String
        """

        return ''.join([chr(int(data[i:i + 8], 2)) for i in range(0, len(data), 8)])


if __name__ == "__main__":
    with open("secret_data.txt", "r") as f:
        secret_data = f.read()

    bits_to_hide = np.random.choice(range(1, 9), np.random.randint(1, 9), replace=False)
    bits_to_hide = list(bits_to_hide)
    bits_to_hide.sort()
    # bits_to_hide = [1]
    print(f"Bits to hide: {bits_to_hide}")

    docx_file = "testfile.docx"
    output_encoded_docx = "encoded_document.docx"


    # Encode data, get as bytes
    encoded_data = docx_steg(docx_file=docx_file, bits_to_hide=bits_to_hide).encode(secret_data=secret_data)

    # Write encoded data to file
    with open(output_encoded_docx, "wb") as f:
        f.write(encoded_data)

    # Decode data from encoded docx file
    decoded_data = docx_steg(docx_file=output_encoded_docx, bits_to_hide=bits_to_hide).decode()

    # Print the decoded data
    print("[+] Decoded data:", decoded_data)
