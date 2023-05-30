from flask import Flask, render_template, request, redirect, session, send_from_directory
from lib.steganography import img_steg
import cv2

WORKING_PATH = 'Application/upload/'

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
    file = request.files['origin']
    b2c = [int(request.form['b2c'])]
    payload = request.form['payload']

    if file.filename != "":
        file.save(WORKING_PATH + file.filename)
        steg = img_steg.img_steg(WORKING_PATH + file.filename, b2c).encode(payload)
        cv2.imwrite(WORKING_PATH + "encoded_" + file.filename, steg)
        session['image'] = file.filename
        session['image2'] = "encoded_" + file.filename
        return redirect("/encode_result")

@app.route('/encode_result')
def encode_result():
    if len(session) > 0:
        return render_template("encode_result.html", image=session.get("image"), image2=session.get('image2'))
    else:
        return redirect("/encode")
 
@app.route('/decode')
def decode():
    session_clear()
    return render_template('decode.html')

@app.route("/decoding", methods=['POST'])
def decoding():
    file = request.files['encoded_file']
    b2c = [int(request.form['b2c'])]
    if file.filename != "":
        file.save(WORKING_PATH + file.filename)
        payload = img_steg.img_steg(WORKING_PATH + file.filename, b2c).decode()
        session["payload"] = payload
        session["image"] = file.filename
        return redirect("/decode_result")

@app.route('/decode_result')
def decode_result():
    if len(session) > 0:
        return render_template("decode_result.html", payload=session.get("payload"), image=session.get("image"))
    else:
        return redirect("/decode")

@app.route('/upload/<path:filename>')
def upload(filename):
    return send_from_directory('upload', filename)

if __name__ == "__main__":
    app.debug = True
    app.run(host="localhost", port=8000)