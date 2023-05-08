from flask import Flask, send_from_directory, request, make_response, jsonify
import subprocess, os, sys, shutil
from esp_polish_transcription import esp_to_polish

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
    esp_txt = request.json['eo_txt']
    pol_txt = request.json['pl_txt']
    voice_name = request.json['voice_name']

    esp_txt = esp_txt.strip()
    pol_txt = pol_txt.strip()
    voice_name = voice_name.strip()

    pol_input_words = pol_txt.split(' ')

    print(esp_txt, pol_txt)

    [esp_txt_out, pol_txt_out] = esp_to_polish(esp_txt)
    
    print(esp_txt_out, pol_txt_out)

    esp_words = esp_txt_out.split(' ')
    pol_words = pol_txt_out.split(' ')
    

    if len(esp_words) != len(pol_words) or len(esp_words) != len(pol_input_words):
        result = {'resp': 'Fail', 'message':'polish transcription failed, number of words is different'}
        resp = make_response(jsonify(result))
        return resp

    # 1. 불필요한 항목은 저장하지 않는다 - 에스페란토 단어(A B C)와 변형된 폴란드어 단어(Ap Bp-x Cp)가 수작업으로 변경 되었으면 Overrides.py에 
    # Append하고 만약에 변경작업을 하지 않았으면 저장하지 않는다.
    # overrides[‘A’] = ‘Ap’는 저장하지 않고, 
    # overrides[‘B] = ‘Bp-x’는 저장한다.
    diff_indexes = []
    for i, word in enumerate(pol_words):
        if word != pol_input_words[i]:
            diff_indexes.append(i)
    print(diff_indexes)
    for diff_index in diff_indexes:
        esp_word = esp_words[diff_index]        
        pol_word = pol_input_words[diff_index] 

        esp_word = esp_word.replace("!", "")
        esp_word = esp_word.replace(",", "")
        esp_word = esp_word.replace(".", "")
        esp_word = esp_word.replace("?", "")
        esp_word = esp_word.replace("~", "")
        esp_word = esp_word.replace(":", "")
        esp_word = esp_word.replace(";", "")
        esp_word = esp_word.replace("(", "")
        esp_word = esp_word.replace(")", "")

        pol_word = pol_word.replace("!", "")
        pol_word = pol_word.replace(",", "")
        pol_word = pol_word.replace(".", "")
        pol_word = pol_word.replace("?", "")
        pol_word = pol_word.replace("~", "")
        pol_word = pol_word.replace(":", "")
        pol_word = pol_word.replace(";", "")
        pol_word = pol_word.replace("(", "")
        pol_word = pol_word.replace(")", "")

        fileobj = open('exception_pol.tsv' ,'a')
        fileobj.write("%s\t%s\n" % (esp_word, pol_word))
        fileobj.close()

    # 2. output.mp3를 ./sound/(voice_name)/(esp_txt).mp3 로 파일 mv/overwrite하기
    mp3_file = "../memlingo/sounds/"+voice_name+'/'+esp_txt+'.mp3'
    if os.path.exists("./output.mp3"):
        shutil.move("./output.mp3", mp3_file)

    
    result = {'resp': 'OK', 'message':'remeber.py sucessfully'}
    resp = make_response(jsonify(result))
    return resp


@app.route('/tts/remember_all.api', methods=['POST'])
def remember_all():
    esp_txt = request.json['eo_txt']
    pol_txt = request.json['pl_txt']

    esp_txt = esp_txt.strip()
    pol_txt = pol_txt.strip()

    voices = ["male1", "male2", "male3", "female1", "female2", "female3", "ludoviko"]
    for voice in voices:
        if voice == "ludoviko":
            cmd = ["python3", "esp_polish_transcription.py", "-e" ,"%s" % esp_txt, "%s" % voice]
        else:
            cmd = ["python3", "esp_polish_transcription.py", "-p" ,"%s" % esp_txt, "%s" % voice]
        output = subprocess.run(cmd, stdout=subprocess.PIPE) 

        # 2. output.mp3를 ./sound/(voice)/(esp_txt).mp3 로 파일 mv/overwrite하기
        mp3_file = "../memlingo/sounds/"+voice+'/'+esp_txt+'.mp3'
        if os.path.exists("./output.mp3"):
            print("mp3_file:"+mp3_file)
            shutil.move("./output.mp3", mp3_file)

    
    result = {'resp': 'OK', 'message':'remeber_all.api sucessfully'}
    resp = make_response(jsonify(result))
    return resp



app.run(debug=True, host='192.168.117.129', port=5001)


