from flask import Flask, render_template, request, redirect, session, send_from_directory
from lib.steganography import img_steg, wav_steg, txt_steg, file_steg
import cv2
import os
import sys
import wave
import warnings

MAX_SESSION_SIZE = 4096 * 3
WORKING_PATH = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "upload") + os.sep

# Supported file extensions
supported_files = {
    "txt_files": ["txt", "py", "sql", "html", "css", "js", "php", "c", "cpp", "java", "json", "xml", "yml", "md"],
    "gen_files": ["mp3", "mp4"],
    "doc_files": ["docx", "xlsx", "pptx", "csv"],
    "wav_files": ["wav"],
    "image_files": ["bmp", "png"]
}

app = Flask(__name__, template_folder='views')
app.secret_key = 'b3a5e8d11fb3d8d3647b6cf2e51ad768'


def session_clear():
    if len(session) > 0:
        session.clear()


@app.route('/')
def modeSelection():
    session_clear()
    return render_template('mode_selection.html')


@app.route('/encode')
def encode():
    session_clear()
    return render_template('encode.html')


@app.route("/encoding", methods=['POST'])
def encoding():
    try:
        file = request.files['origin']
        b2c = [int(x) for x in request.form.getlist("b2c")]
        # Sort b2c in ascending order
        b2c.sort()
        payload = request.form['payload']

        if file.filename != "":
            file.save(WORKING_PATH + file.filename)

            file_extension = os.path.splitext(file.filename)[1][1:]
            if file_extension in supported_files["image_files"]:
                encode = img_steg.img_steg(WORKING_PATH + file.filename, b2c).encode(payload)
                cv2.imwrite(WORKING_PATH + "encoded_" + file.filename, encode)
                session['image'] = file.filename
                session['image2'] = "encoded_" + file.filename
            elif file_extension in supported_files["wav_files"]:
                encode = wav_steg.wav_steg(WORKING_PATH + file.filename, b2c).encode(payload)

                # Write encoded data to file
                new_wav_file = wave.open(WORKING_PATH + "encoded_" + file.filename, "wb")
                new_wav_file.setnchannels(encode["num_channels"])
                new_wav_file.setsampwidth(encode["sample_width"])
                new_wav_file.setframerate(encode["frame_rate"])
                new_wav_file.writeframes(encode["num_frames"])
                new_wav_file.close()
                session['wav'] = file.filename
                session['wav2'] = "encoded_" + file.filename
            elif file_extension in supported_files["txt_files"]:
                encoded_data = txt_steg.txt_steg(WORKING_PATH + file.filename, b2c).encode(payload)
                with open(os.path.join(WORKING_PATH, "encoded_" + file.filename), "w") as f:
                    f.write(encoded_data)
                session['txt'] = file.filename
                session['txt2'] = "encoded_" + file.filename
            elif file_extension in supported_files["gen_files"] + supported_files["doc_files"]:
                encoded_data = file_steg.file_steg(WORKING_PATH + file.filename, b2c).encode(payload)
                with open(os.path.join(WORKING_PATH, "encoded_" + file.filename), "wb") as f:
                    f.write(encoded_data)
                if file_extension in supported_files["doc_files"]:
                    file_extension = "document"
                session[file_extension] = file.filename
                session[file_extension + '_2'] = "encoded_" + file.filename
            else:
                print(f"Unsupported file extension: {file_extension}")
                return redirect("/unsupported")

        return redirect("/encode_result")
    except Exception as exception:
        print("ENCODE(Exception):", exception)
        return redirect("/unsupported")
    except UserWarning as warning:
        print("ENCODE(warning):", warning)
        return redirect("/unsupported")


@app.route('/encode_result')
def encode_result():
    if len(session) > 0:
        return render_template("encode_result.html")
    else:
        return redirect("/encode")


@app.route('/decode')
def decode():
    session_clear()
    return render_template('decode.html')


@app.route("/decoding", methods=['POST'])
def decoding():
    def decode_files(class_name, _path, b2c, ext):
        class_name_str = class_name.__name__.split(".")[-1]
        method = getattr(class_name, class_name_str)
        payload = method(_path, b2c).decode()

        if class_name_str == "img_steg":
            session["image"] = file.filename
        elif ext in supported_files["doc_files"]:
            session["document"] = file.filename
        elif ext in supported_files["txt_files"]:
            session["txt"] = file.filename
        else:
            session[ext] = file.filename

        if sys.getsizeof(payload) <= MAX_SESSION_SIZE:
            session["payload"] = payload
        else:
            raise Exception("Payload too big")

    try:
        file = request.files['encoded_file']
        b2c = [int(x) for x in request.form.getlist("b2c")]
        # Sort b2c in ascending order
        b2c.sort()
        if file.filename != "":
            _path = WORKING_PATH + file.filename

            file.save(_path)

            file_extension = os.path.splitext(file.filename)[1][1:]
            if file_extension in supported_files["image_files"]:
                decode_files(img_steg, _path, b2c, file_extension)
            elif file_extension in supported_files["wav_files"]:
                decode_files(wav_steg, _path, b2c, file_extension)
            elif file_extension in supported_files["txt_files"]:
                decode_files(txt_steg, _path, b2c, file_extension)
            elif file_extension in supported_files["gen_files"] + supported_files["doc_files"]:
                decode_files(file_steg, _path, b2c, file_extension)
            else:
                print(f"Unsupported file extension: {file_extension}")
                return redirect("/unsupported")

        return redirect("/decode_result")
    except Exception as exception:
        print("DECODE(Exception):", exception)
        return redirect("/unsupported")
    except UserWarning as warning:
        print("DECODE(warning):", warning)
        return redirect("/unsupported")


@app.route('/decode_result')
def decode_result():
    if len(session) > 0:
        return render_template("decode_result.html")
    else:
        return redirect("/decode")


@app.route('/unsupported')
def unsupported():
    return render_template('unsupported.html')


@app.route('/get_session')
def get_session():
    session_data = dict(session)
    return session_data


@app.route('/upload/<path:filename>')
def upload(filename):
    return send_from_directory('upload', filename)


if __name__ == "__main__":
    app.debug = True
    app.run(host="localhost", port=8000)
