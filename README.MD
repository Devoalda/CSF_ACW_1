# LSB Replacement with Python
This is an LSB Replacement project built with python and flask. 

## Installation
```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage
```bash
python lsb_rep.py
```
# Supported File Types
## Image
- PNG
- BMP

These are the only two image types that are tested and supported.

## Audio-Visual
- WAV
- MP3
- MP4

WAV uses the `wav_steg` module in `lib/steganography` and MP3 and MP4 uses the general `file_steg` module in `lib/steganography`.

## Document
### Text Files
- TXT
- PY
- MD
- ETC.

These files are supported by the `txt_steg` module in `lib/`.

### Others
- PDF
- DOCX
- PPTX
- ETC.

These files are supported by the `file_steg` module in `lib/steganography`. 

# Modules
All modules are located in the `lib/steganography` folder.

## `img_steg`
This module is used to hide and extract data from images using the opencv and numpy libraries for bit manipulation.

Usage:
```python
from lib.steganography import img_steg

encoded_data = img_steg("/path/to/image.png", bits_to_hide=[1,2,3]).encode("Hello World!")
decoded_data = img_steg("/path/to/encoded_image.png", bits_to_hide=[1,2,3]).decode()
```

## `wav_steg`
This module is used to hide and extract data from WAV files using the wave library for wav file manipulation.

Usage:
```python
from lib.steganography import wav_steg

encoded_data = wav_steg("/path/to/audio.wav", bits_to_hide=[1,2,3]).encode("Hello World!")
decoded_data = wav_steg("/path/to/encoded_audio.wav", bits_to_hide=[1,2,3]).decode()
```

## `txt_steg`
This module is used to hide and extract data from text files with python's built in file reading and writing.

Usage:
```python
from lib.steganography import txt_steg

encoded_data = txt_steg("/path/to/text.txt", bits_to_hide=[1,2,3]).encode("Hello World!")
decoded_data = txt_steg("/path/to/encoded_text.txt", bits_to_hide=[1,2,3]).decode()
```

## `file_steg`
This module is used to hide and extract data from any file type with python's built in file reading and writing as bytes.

Usage:
```python
from lib.steganography import file_steg

encoded_data = file_steg("/path/to/file.txt", bits_to_hide=[1,2,3]).encode("Hello World!")
decoded_data = file_steg("/path/to/encoded_file.txt", bits_to_hide=[1,2,3]).decode()
```

# Web Interface
The web interface is built with flask and located at project root. The web interface is used as a front end to hide and extract data from files.

## Views
Views (HTML) are located in the `views` folder.

## Routes
```
/ - Home page
/encode - Encode page
/decode - Decode page
```

## Encode
The encode page is used to encode data into a file. 

User is able to:
- Select a file to encode data into (Drag and drop supported)
- Select the bits to hide the data in
- Enter the data to hide
- Submit the form
- Download the encoded file
- View the encoded file
- View the original file

## Decode
The decode page is used to decode data from a file.

User is able to:
- Select a file to decode data from
- Select the bits to decode the data from
- Submit the form
- View the decoded data

## Sample files for testing
Sample files are in the `upload` folder, these files are used for testing the web interface and the individual modules.