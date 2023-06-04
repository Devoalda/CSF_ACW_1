import cv2
import numpy as np


class img_steg:
    def __init__(self, image_name: str = None, bit_to_hide: list[int] = None) -> None:
        """
        Initialize the class
        :param image_name:  Name of the image to encode or decode
        :type image_name: str
        :param bit_to_hide: List of bit position to hide the data (LSB is 1, MSB is 8) Default is LSB (index = 7)
        :type bit_to_hide: list[int]
        """
        if image_name:
            self.image_name = image_name
        else:
            raise FileNotFoundError("[!] Please specify an image file")

        self.bit_to_hide = [8 - bit_pos for bit_pos in bit_to_hide] if bit_to_hide else [
            7]  # Default is LSB (index = 7)
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
        n_bits = (image.shape[0] * image.shape[1] * 3) * 8 * len(self.bit_to_hide)  # Max bits to encode

        secret_data += self.delimiter  # Add delimiter at the end of data

        if len(secret_data) * 8 > n_bits:
            raise ValueError("[!] Insufficient bytes, need a bigger image or less data")

        # Convert bit to hide position
        data_index = 0
        binary_secret_data = self.to_bin(secret_data)  # Convert data to binary
        data_len = len(binary_secret_data)  # size of data to hide

        for row in image:
            for pixel in row:
                r, g, b = self.to_bin(pixel)  # Convert RGB Values to binary format
                for bit_pos in self.bit_to_hide:
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

        return image

    def decode(self) -> str:
        """
        Decode the data hidden in the image

        :return: Decoded Data: String
        """
        image = cv2.imread(self.image_name)  # read image
        binary_data = ""

        for row in image:
            for pixel in row:
                r, g, b = self.to_bin(pixel)
                for bit_pos in self.bit_to_hide:
                    binary_data += r[bit_pos]  # retrieve data from specified bit position of red pixel
                    binary_data += g[bit_pos]  # retrieve data from specified bit position of green pixel
                    binary_data += b[bit_pos]  # retrieve data from specified bit position of blue pixel

        # Split by 8 bits
        all_bytes = [binary_data[i: i + 8] for i in range(0, len(binary_data), 8)]
        # Convert from bits to characters
        decoded_data = ""
        for byte in all_bytes:
            decoded_data += chr(int(byte, 2))
            if decoded_data[-len(self.delimiter):] == self.delimiter:
                break

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


def main():
    raise NotImplementedError("This module is not meant to run by itself")


if __name__ == "__main__":
    main()
