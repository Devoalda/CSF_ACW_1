import cv2
import numpy as np


class img_steg:
    def __init__(self, image_name: str = "image.png", bit_to_hide: list[int] = None) -> None:
        """
        Initialize the class
        :param image_name:  Name of the image to encode or decode
        :type image_name: str
        :param bit_to_hide: List of bit position to hide the data (LSB is 1, MSB is 8)
        :type bit_to_hide: list[int]
        """
        self.image_name = image_name
        self.bit_to_hide = [8 - bit_pos for bit_pos in bit_to_hide] if bit_to_hide else [1]  # Default is LSB
        self.delimiter = "abc-123-a=="

    def encode(self, secret_data: str = "Hello World") -> np.ndarray:
        """
        Encode the secret data in the image
        :param secret_data: Data to hide in the image
        :type secret_data: str
        :return: Encoded Image
        :rtype: np.ndarray
        """
        image = cv2.imread(self.image_name)  # read image
        n_bytes = image.shape[0] * image.shape[1] * 3 // 8  # Max bytes to encode
        print("[*] Maximum bytes to encode:", n_bytes)
        secret_data += self.delimiter  # Add delimiter at the end of data
        if len(secret_data) > n_bytes:
            raise ValueError("[!] Insufficient bytes, need a bigger image or less data")
        print("[*] Encoding Data...")

        # Convert bit to hide position
        bit_to_hide = self.bit_to_hide
        data_index = 0
        binary_secret_data = self.to_bin(secret_data)  # Convert data to binary
        data_len = len(binary_secret_data)  # size of data to hide

        print(f"[+] Size of data to hide: {data_len}")
        print("[+] Starting encoding...")

        for row in image:
            for pixel in row:
                r, g, b = self.to_bin(pixel)  # Convert RGB Values to binary format
                for bit_pos in bit_to_hide:
                    if data_index < data_len:
                        r = list(r)
                        r[bit_pos] = binary_secret_data[
                            data_index]  # hide data into specified bit position of red pixel
                        pixel[0] = int(''.join(r), 2)
                        data_index += 1
                    if data_index < data_len:
                        g = list(g)
                        g[bit_pos] = binary_secret_data[
                            data_index]
                        pixel[1] = int(''.join(g), 2)
                        data_index += 1
                    if data_index < data_len:
                        b = list(b)
                        b[bit_pos] = binary_secret_data[
                            data_index]
                        pixel[2] = int(''.join(b), 2)
                        data_index += 1
                    if data_index >= data_len:
                        break
                pixel[0] = int(''.join(r), 2)  # convert modified binary back to integer for red pixel
                pixel[1] = int(''.join(g), 2)  # convert modified binary back to integer for green pixel
                pixel[2] = int(''.join(b), 2)  # convert modified binary back to integer for blue pixel

                if data_index >= data_len:
                    break

        print(f"[+] Encoding completed")

        return image

    def decode(self) -> str:
        """
        Decode the data hidden in the image

        :return: Decoded Data: String
        """
        print("[+] Decoding...")
        image = cv2.imread(self.image_name)  # read image
        binary_data = ""
        bit_to_hide = self.bit_to_hide

        print(f"[+] Extracting data from image...")
        for row in image:
            for pixel in row:
                r, g, b = self.to_bin(pixel)
                for bit_pos in bit_to_hide:
                    binary_data += r[bit_pos]  # retrieve data from specified bit position of red pixel
                    binary_data += g[bit_pos]  # retrieve data from specified bit position of green pixel
                    binary_data += b[bit_pos]  # retrieve data from specified bit position of blue pixel

        print(f"[+] Forming binary data completed")
        print(f"[+] Decoding binary data...")

        # Split by 8 bits
        all_bytes = [binary_data[i: i + 8] for i in range(0, len(binary_data), 8)]
        # Convert from bits to characters
        decoded_data = ""
        for byte in all_bytes:
            decoded_data += chr(int(byte, 2))
            if decoded_data[-len(self.delimiter):] == self.delimiter:
                break

        print(f"[+] Decoding completed")
        return decoded_data[:-len(self.delimiter)]

    def to_bin(self, data: str) -> str | list[str]:
        """
        Convert data to binary format as string

        :param data: Data to convert
        :type data: str
        :return: Binary Data
        :rtype: str | list[str]
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
        # UNUSED
        Convert binary `data` back to the original format

        :param data: Binary Data
        :type data: str
        :return: Original Data
        :rtype: str
        """
        return ''.join([chr(int(data[i:i + 8], 2)) for i in range(0, len(data), 8)])


def main():
    # Variables
    image_name = "test.bmp"
    encoded_image_name = "encoded_image.bmp"
    secret_data = ""
    with open("../Txt_Steg/secret_data.txt", "r") as f:
        secret_data = f.read()

    # Generate random bit positions to hide data into image for testing
    bit_to_hide = np.random.choice(range(1, 9), np.random.randint(1, 9), replace=False)
    bit_to_hide = list(bit_to_hide)
    bit_to_hide.sort()
    print(f"Bits to hide: {bit_to_hide}")

    print("Welcome to Image Steganography")

    # Encode the data into the image
    encoded_image = img_steg(image_name=image_name, bit_to_hide=bit_to_hide).encode(secret_data)
    cv2.imwrite(encoded_image_name, encoded_image)

    # Decode the data from the image
    decoded_data = img_steg(image_name=encoded_image_name, bit_to_hide=bit_to_hide).decode()
    print("Decoded Data:", decoded_data)


if __name__ == "__main__":
    main()

##############################
#  _   _
# | | | |___  __ _  __ _  ___
# | | | / __|/ _` |/ _` |/ _ \
# | |_| \__ \ (_| | (_| |  __/
#  \___/|___/\__,_|\__, |\___|
#                  |___/
##############################
#
# Initialise class with image name and bit to hide
#
# image_name = image name with extension (String)
# bit_to_hide = [1, 2, 3] (Please Sort the list in ascending order)
#
# To encode:
# encoded_image = img_steg(image_name, bit_to_hide).encode(secret_data)
#
# To decode:
# decoded_data = img_steg(image_name, bit_to_hide).decode()
# Both are string types
