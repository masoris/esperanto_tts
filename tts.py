from flask import Flask, send_from_directory, request, make_response, jsonify
import subprocess, os

app = Flask(__name__)

@app.route('/tts/<path:path>')
def serve_tts(path):
    return send_from_directory('.', path)

@app.route('/tts/speak.api', methods=['POST'])
def speak():
    lang = request.json['lang']
    voicename = request.json['voicename']
    textdata = request.json['textdata']

    if lang == "eo":
        cmd = ["python3", "esp_polish_transcription.py", "-e" ,"%s" % textdata, "%s" % voicename]
    else:
        cmd = ["python3", "esp_polish_transcription.py", "-p" ,"%s" % textdata, "%s" % voicename]
    # print(cmd)
    output = subprocess.run(cmd, stdout=subprocess.PIPE) 
    # print(output.stdout.decode('utf-8'))

    lines = output.stdout.decode('utf-8').split('\n')
    print (lines)
    esp_txt = None
    for line in lines:
        if line.find("pol_txt=") == 0:
            pol_txt = line[8:]
        if line.find("esp_txt=") == 0:
            esp_txt = line[8:]

    if esp_txt is not None:
        result = {'resp': 'OK', 'lang':lang, 'voicename':voicename, 'textdata':textdata, 'pol_txt':pol_txt, 'esp_txt': esp_txt}
    else:
        result = {'resp': 'OK', 'lang':lang, 'voicename':voicename, 'textdata':textdata, 'pol_txt':pol_txt}
    resp = make_response(jsonify(result))
    return resp

@app.route('/tts/remember.api', methods=['POST'])
def remember():
    eo_txt = request.json['eo_txt']
    pl_txt = request.json['pl_txt']
    voice_name = request.json['voice_name']
    
    cmd = ["python3", "remember.py", eo_txt , pl_txt, voice_name]
    output = subprocess.run(cmd, stdout=subprocess.PIPE) 
    print(output)
    
    result = {'resp': 'OK', 'message':'remeber.py sucessfully'}
    resp = make_response(jsonify(result))
    return resp

app.run(debug=True, host='192.168.117.129', port=5001)


