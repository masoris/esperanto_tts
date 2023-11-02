from flask import Flask, send_from_directory, request, make_response, jsonify
import subprocess
import os
import sys
import shutil
import random
from transcription import esp_to_polish, get_esp_mp3_file, get_pol_mp3_file

app = Flask(__name__)


@app.route('/tts/<path:path>')
def serve_tts(path):
    return send_from_directory('.', path)

# favicon.ico 파일 서비스


@app.route('/favicon.ico')
def serve_favicon():
    return send_from_directory('.', 'favicon.ico')


@app.route('/tts/speak.api', methods=['POST'])
def speak():
    lang = request.json['lang']
    voicename = request.json['voicename']
    textdata = request.json['textdata']

    if lang == "eo":
        cmd = ["python3", "transcription.py",
               "-e", textdata, voicename]
    else:
        cmd = ["python3", "transcription.py",
               "-p", textdata, voicename]
    # print(cmd)
    output = subprocess.run(cmd, stdout=subprocess.PIPE)
    # print(output.stdout.decode('utf-8'))

    lines = output.stdout.decode('utf-8').split('\n')
    print(lines)
    esp_txt = None
    for line in lines:
        if line.find("pol_txt=") == 0:
            pol_txt = line[8:]
        if line.find("esp_txt=") == 0:
            esp_txt = line[8:]

    if esp_txt is not None:
        result = {'resp': 'OK', 'lang': lang, 'voicename': voicename,
                  'textdata': textdata, 'pol_txt': pol_txt, 'esp_txt': esp_txt}
    else:
        result = {'resp': 'OK', 'lang': lang, 'voicename': voicename,
                  'textdata': textdata, 'pol_txt': pol_txt}
    resp = make_response(jsonify(result))
    return resp


@app.route('/tts/get_voices.api', methods=['POST'])
def get_voices():
    wordlist = request.json['wordlist']

    word_voice_pairs = []
    voices = ["male1", "male2", "female1",
              "female2", "ludoviko"]

    for word in wordlist:
        voice_list = ""
        for voice in voices:
            if os.path.exists("../memlingo/sounds/"+voice+"/"+word+".mp3"):
                voice_list += voice + ","
        word_voice_pair = [word, voice_list]
        word_voice_pairs.append(word_voice_pair)

    result = {'word_voice_pairs': word_voice_pairs}

    resp = make_response(jsonify(result))
    return resp


@app.route('/tts/remember.api', methods=['POST'])
def remember():
    esp_txt = request.json['eo_txt']
    pol_txt = request.json['pl_txt']
    voice_name = request.json['voice_name']
    filename = request.json['filename']

    esp_txt = esp_txt.strip()
    pol_txt = pol_txt.strip()
    voice_name = voice_name.strip()
    filename = filename.strip()

    pol_input_words = pol_txt.split(' ')

    print(esp_txt, pol_txt)

    [esp_txt_out, pol_txt_out] = esp_to_polish(esp_txt)

    print(esp_txt_out, pol_txt_out)

    esp_words = esp_txt_out.split(' ')
    pol_words = pol_txt_out.split(' ')

    if len(esp_words) != len(pol_words) or len(esp_words) != len(pol_input_words):
        result = {'resp': 'Fail',
                  'message': 'polish transcription failed, number of words is different'}
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
        esp_word = esp_word.replace("\"", "")

        pol_word = pol_word.replace("!", "")
        pol_word = pol_word.replace(",", "")
        pol_word = pol_word.replace(".", "")
        pol_word = pol_word.replace("?", "")
        pol_word = pol_word.replace("~", "")
        pol_word = pol_word.replace(":", "")
        pol_word = pol_word.replace(";", "")
        pol_word = pol_word.replace("(", "")
        pol_word = pol_word.replace(")", "")
        pol_word = pol_word.replace("\"", "")

        fileobj = open('exception_pol.tsv', 'a')
        fileobj.write("%s\t%s\n" % (esp_word, pol_word))
        fileobj.close()

    # 2. output.mp3를 ./sound/(voice_name)/(esp_txt).mp3 로 파일 mv/overwrite하기
    mp3_file = "../memlingo/sounds/"+voice_name+'/'+filename+'.mp3'
    if os.path.exists("./output.mp3"):
        shutil.move("./output.mp3", mp3_file)

    result = {'resp': 'OK', 'message': 'remeber.py sucessfully'}
    resp = make_response(jsonify(result))
    return resp

def remember_all_args(esp_txt, pol_txt, filename):
    esp_txt = esp_txt.strip()
    pol_txt = pol_txt.strip()
    filename = filename.strip()

    # male = random.choice(["male1", "male2"])
    # female = random.choice(["female1", "female2"])
    voices = ["male1", "male2", "female1", "female2", "ludoviko"]
    for voice in voices:
        if voice == "ludoviko":
            get_esp_mp3_file("ludoviko", esp_txt, "output.mp3")
            # cmd = ["python3", "transcription.py",
            #        "-e", "%s" % esp_txt, "%s" % voice]
        else:
            get_pol_mp3_file(voice, pol_txt, "output.mp3")
            # cmd = ["python3", "transcription.py",
            #    "-p", "%s" % pol_txt, "%s" % voice]
        # output = subprocess.run(cmd, stdout=subprocess.PIPE)

        # 2. output.mp3를 ./sound/(voice)/(esp_txt).mp3 로 파일 mv/overwrite하기
        mp3_file = "../memlingo/sounds/"+voice+'/'+filename+'.mp3'
        if os.path.exists("./output.mp3"):
            print("mp3_file:"+mp3_file)
            if os.path.exists(mp3_file):
                os.remove(mp3_file)
            # ludoviko는 h가 들어가는 발음을 제대로 못함, 그래서 저장하지 않음
            if (esp_txt.find("h") >= 0 or esp_txt.find("H") >= 0) and voice == "ludoviko":
                pass
            else:
                shutil.move("./output.mp3", mp3_file)


@app.route('/tts/remember_all.api', methods=['POST'])
def remember_all():
    esp_txt = request.json['eo_txt']
    pol_txt = request.json['pl_txt']
    filename = request.json['filename']

    remember_all_args(esp_txt, pol_txt, filename)
    
    result = {'resp': 'OK', 'message': 'remeber_all.api sucessfully'}
    resp = make_response(jsonify(result))
    return resp


@app.route('/tts/remove_all.api', methods=['POST'])
def remove_all():
    esp_txt = request.json['eo_txt']
    pol_txt = request.json['pl_txt']
    filename = request.json['filename']

    esp_txt = esp_txt.strip()
    pol_txt = pol_txt.strip()
    filename = filename.strip()

    voices = ["male1", "male2", "female1",
              "female2", "ludoviko"]
    for voice in voices:

        # ./sound/(voice)/(esp_txt).mp3의 파일을 삭제하기
        mp3_file = "../memlingo/sounds/"+voice+'/'+filename+'.mp3'
        if os.path.exists(mp3_file):
            os.remove(mp3_file)

    result = {'resp': 'OK', 'message': 'remove_all.api sucessfully'}
    resp = make_response(jsonify(result))
    return resp


# app.run(debug=True, host='localhost', port=5001)
