from flask import Flask, render_template, request, redirect
app = Flask(__name__, template_folder='views')

@app.route('/')
def modeSelection():
    return render_template('mode_selection.html')

@app.route('/encode')
def encode():
    return render_template('encode.html')

@app.route("/encoding", methods=['POST'])
def encoding():
    file = request.files['origin']
    payload = request.form['payload']

    if file.filename != "":
        file.save('upload/' + file.filename)

        # run the encoding function 
        #return encoded file to the result below
        return redirect("/encode_result")

@app.route('/encode_result')
def encode_result():
    return render_template("encode_result.html")

@app.route('/decode')
def decode():
    return render_template('decode.html')

@app.route("/decoding", methods=['POST'])
def decoding():
    file = request.files['encoded_file']

    if file.filename != "":
        file.save('upload/' + file.filename)
        
        # run the decoding function 
        #return decoded payload to the result below
        return redirect("/decode_result")

@app.route('/decode_result')
def decode_result():
    return render_template("decode_result.html")

if __name__ == "__main__":
    app.debug = True
    app.run(host="localhost", port=8000)