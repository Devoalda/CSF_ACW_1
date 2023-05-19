import cv2
import numpy as np


class img_steg:
    def __init__(self, image_name: str = "image.png", bit_to_hide: int = 2):
        self.image_name = image_name
        self.bit_to_hide = bit_to_hide

    def to_bin(self, data: str) -> str | list[str]:
        """
        Convert data to binary format as string
        Args:
            data: String

        Returns:
            Binary Data: String | List[String]
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
        Args:
            data: String

        Returns:
            Original Data: String
        """
        return ''.join([chr(int(data[i:i + 8], 2)) for i in range(0, len(data), 8)])

    def decode(self):
        """
        Decode the data hidden in the image
        Returns:
            Decoded Data: str
        """
        print("[+] Decoding...")
        image = cv2.imread(self.image_name)  # read image
        binary_data = ""
        for row in image:
            for pixel in row:
                r, g, b = self.to_bin(pixel)
                binary_data += r[self.bit_to_hide]
                binary_data += g[self.bit_to_hide]
                binary_data += b[self.bit_to_hide]
        # Split by 8 bits
        all_bytes = [binary_data[i: i + 8] for i in range(0, len(binary_data), 8)]
        # Convert from bits to characters
        decoded_data = self.from_bin(''.join(all_bytes))
        if decoded_data.endswith("===="):
            decoded_data = decoded_data[:-4]
        return decoded_data

    def encode(self, secret_data: str = "Hello World") -> np.ndarray:
        """
       Encode the secret data in the image
       Args:
           secret_data: str

       Returns:
           Encoded Image: np.ndarray
       """
        image = cv2.imread(self.image_name)  # read image
        n_bytes = image.shape[0] * image.shape[1] * 3 // 8  # Max bytes to encode
        print("[*] Maximum bytes to encode:", n_bytes)
        secret_data += "===="  # Stopping Criteria
        if len(secret_data) > n_bytes:
            raise ValueError("[!] Insufficient bytes, need a bigger image or less data")
        print("[*] Encoding Data...")

        # Convert bit to hide position
        bit_to_hide = 2 - self.bit_to_hide
        data_index = 0
        binary_secret_data = self.to_bin(secret_data)  # Convert data to binary
        data_len = len(binary_secret_data)  # size of data to hide
        for row in image:
            for pixel in row:
                r, g, b = self.to_bin(pixel)  # Convert RGB Values to binary format
                if data_index < data_len:
                    r = list(r)
                    r[bit_to_hide] = binary_secret_data[data_index]  # hide data into least significant bit of red pixel
                    pixel[0] = int(''.join(r), 2)
                    data_index += 1
                if data_index < data_len:
                    g = list(g)
                    g[bit_to_hide] = binary_secret_data[data_index]
                    pixel[1] = int(''.join(g), 2)
                    data_index += 1
                if data_index < data_len:
                    b = list(b)
                    b[bit_to_hide] = binary_secret_data[data_index]
                    pixel[2] = int(''.join(b), 2)
                    data_index += 1
                if data_index >= data_len:
                    break
        return image


def main():
    print("Welcome to Image Steganography")
    print("1. Encode\n2. Decode\n3. Exit")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        image_name = input("Enter name of image to encode: ")
        secret_data = input("Enter data to encode: ")
        bit_to_hide = int(input("Enter bit to hide (1-8): "))
        encoded_image = img_steg(image_name, bit_to_hide).encode(secret_data)
        cv2.imwrite("encoded_image.png", encoded_image)
        print("Image Encoded Successfully")
    elif choice == 2:
        image_name = input("Enter name of image to decode: ")
        bit_to_hide = int(input("Enter bit to hide (1-8): "))
        decoded_data = img_steg(image_name, bit_to_hide).decode()
        print("Decoded Data:", decoded_data)


if __name__ == "__main__":
    main()
    
# FOR REFERENCE
# Welcome to Image Steganography
# 1. Encode
# 2. Decode
# 3. Exit
# Enter your choice: 2
# Enter name of image to decode: encoded_image.png
# Enter bit to hide (1-8): 5
# [+] Decoding...
# Decoded Data: abc123abcasdf====