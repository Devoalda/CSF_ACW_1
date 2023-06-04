import wave
import numpy as np


class wav_steg:

    def __init__(self, wav_file: str = "sample.wav", bits_to_hide: list[int] = None) -> None:
        """
        Initialize the class
        :param wav_file: PathName of the wav file to encode or decode
        :type wav_file: str
        :param bits_to_hide: Bit to hide the data in (1 - LSB to 8 - MSB)
        :type bits_to_hide: list[int]
        """
        self.wav_file = wav_file
        self.bits_to_hide = [
            8 - bit_pos for bit_pos in bits_to_hide] if bits_to_hide else [7]  # Default is LSB (index = 7)
        self.delimiter = "====="  # Delimiter to indicate the end of the secret data
        print(self.bits_to_hide)

    def encode(self, secret_data: str = "Hello World") -> dict:
        """
        Encode the secret data into the wav file

        :param secret_data: String of data to hide

        :return: Encoded wav file parameters
        :rtype: dict
        """

        # Read wav file
        try:
            wav_file = wave.open(self.wav_file, 'rb')
        except:
            raise FileNotFoundError("File not found")

        # Get the audio file's parameters
        num_channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        frame_rate = wav_file.getframerate()
        num_frames = wav_file.getnframes()

        # Read all the audio frames
        data = wav_file.readframes(num_frames)

        #Add delimiter
        secret_data+=self.delimiter

        # Max Bits to encode
        n_bits = (len(data) // 8) * len(self.bits_to_hide)

        # Check if secret data can be encoded into wav file
        # print(f"Secret data length: {len(secret_data)}, Max data length: {n_bytes}")
        if len(secret_data)*8 > n_bits:
            raise ValueError(
                f"[-] Error: Binary Secret data length {len(secret_data)*8} is greater than data length {n_bits}")

        # Convert secret data to binary
        binary_secret_data = self.to_bin(secret_data)

        data_index = 0
        encoded_data = bytearray()

        print(f"[+] Starting encoding...")
        # Encode data into wav
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

        new_wav_dict = {
            "num_channels": num_channels,
            "sample_width": sample_width,
            "frame_rate": frame_rate,
            "num_frames": bytes(encoded_data)
        }
        return new_wav_dict

    def decode(self) -> str:
        """
        Decode the secret data from the wav file
        :return: Decoded secret data
        :rtype: str
        """
       # Read wav file
        try:
            modified_wav_file = wave.open(self.wav_file, 'rb')
        except:
            raise FileNotFoundError("File not found")

        # Get the audio parameters
        num_frames = modified_wav_file.getnframes()

        # Read the audio samples
        data = modified_wav_file.readframes(num_frames)

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

        all_bytes = [binary_data[i: i + 8]
                     for i in range(0, len(binary_data), 8)]

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
    raise NotImplementedError("This module is not meant to be run as a script")
