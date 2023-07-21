import googletts
import sys
import csv
import re
# from playsound import playsound


def load_exception():
    exception_esp = {}
    with open('exception_esp.tsv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        for row in reader:
            # if len(row) < 2:
            #     continue
            exception_esp[row[0]] = row[1]

    exception_pol = {}
    with open('exception_pol.tsv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        for row in reader:
            # if len(row) < 2:
            #     continue
            exception_pol[row[0]] = row[1]
    return [exception_esp, exception_pol]


def normalize_esp_text(esp_txt):
    esp_txt = esp_txt.lower()

    # x를 삿갓문자로 바꾼다.
    esp_txt = esp_txt.replace("cx", "ĉ")
    # esp_txt = esp_txt.replace("Cx", "Ĉ")
    esp_txt = esp_txt.replace("gx", "ĝ")
    # esp_txt = esp_txt.replace("Gx", "Ĝ")
    esp_txt = esp_txt.replace("hx", "ĥ")
    # esp_txt = esp_txt.replace("Hx", "Ĥ")
    esp_txt = esp_txt.replace("jx", "ĵ")
    # esp_txt = esp_txt.replace("Jx", "Ĵ")
    esp_txt = esp_txt.replace("ux", "ŭ")
    # esp_txt = esp_txt.replace("Ux", "Ŭ")
    esp_txt = esp_txt.replace("sx", "ŝ")
    # esp_txt = esp_txt.replace("Sx", "Ŝ")

    esp_txt = esp_txt.replace("!", " ! ")
    esp_txt = esp_txt.replace(",", " , ")
    esp_txt = esp_txt.replace(".", " . ")
    esp_txt = esp_txt.replace("?", " ? ")
    # esp_txt = esp_txt.replace("~", " ")
    esp_txt = esp_txt.replace(":", " : ")
    esp_txt = esp_txt.replace(";", " ; ")
    esp_txt = esp_txt.replace("(", " ( ")
    esp_txt = esp_txt.replace(")", " ) ")
    esp_txt = esp_txt.replace("\"", " \" ")

    esp_txt = esp_txt.strip()
    esp_txt = re.sub('\s+', ' ', esp_txt)

    return esp_txt


def esp_to_polish(esp_txt):
    [exception_esp, exception_pol] = load_exception()
    esp_txt = normalize_esp_text(esp_txt)

    # 1 > unu, s-ro > sinjoro 등을 바꾼다
    esp_words = esp_txt.split(" ")
    for i, esp_word in enumerate(esp_words):
        if esp_word in exception_esp:
            esp_words[i] = exception_esp[esp_word]
    esp_txt = " ".join(esp_words)

    # 특수문자로 공백으로 분리한 esp_txt
    org_esp_txt = esp_txt

    # esperanto입력 문장을 음절 단위로 분해해서 분리기호 ェ를 끼워넣는다.
    esp_txt = esp_txt.replace("a", "aェ")
    # esp_txt = esp_txt.replace("A", "A-")
    esp_txt = esp_txt.replace("e", "eェ")
    # esp_txt = esp_txt.replace("E", "E-")
    esp_txt = esp_txt.replace("i", "iェ")
    # esp_txt = esp_txt.replace("I", "I-")
    esp_txt = esp_txt.replace("o", "oェ")
    # esp_txt = esp_txt.replace("O", "O-")
    esp_txt = esp_txt.replace("u", "uェ")
    # esp_txt = esp_txt.replace("U", "U-")

    words = esp_txt.split(" ")
    words2 = []
    for word in words:
        if len(word) >= 2:
            if word[-2] == 'ェ':  # ェ는 분리기호
                word = word[0:-2] + word[-1:]  # 끝에서 2번째 글자가 분리기호면 이어붙임
                words2.append(word)
                continue
        if len(word) >= 1:
            if word[-1] == 'ェ':  # ェ는 분리기호
                word = word[0:-1]  # 마지막 글자가 분리기호면 제거함
        words2.append(word)

    esp_txt = " ".join(words2)
    # return esp_txt

    # 폴란드어 문자 변형 규칙을 반영한다.
    esp_txt = esp_txt.replace('c', 'ts')
    esp_txt = esp_txt.replace('ĉ', 'cz')
    esp_txt = esp_txt.replace('ĝ', 'dż')
    esp_txt = esp_txt.replace('ĥ', 'ch')
    esp_txt = esp_txt.replace('j', 'y')
    # esp_txt = esp_txt.replace('i', 'ij')
    esp_txt = esp_txt.replace('ĵ', 'ż')
    esp_txt = esp_txt.replace('ŝ', 'sz')
    esp_txt = esp_txt.replace('ŭ', 'ł')
    # esp_txt = esp_txt.replace('v', 'w')
    esp_txt = esp_txt.replace('uy', 'ui')

    # 에스페란토 억양을 반영한다.
    words = esp_txt.split(" ")
    words2 = []
    for word in words:
        sylables = word.split('ェ')  # 분리기호 단위로 어절을 나눈다
        if len(sylables) >= 2:  # 끝에서 2번째 음절은 장음으로 발음하게 한다.
            # sylables[-2] = sylables[-2].replace('a', 'aa')
            # sylables[-2] = sylables[-2].replace('e', 'ee')
            # sylables[-2] = sylables[-2].replace('i', 'iy')
            # sylables[-2] = sylables[-2].replace('o', 'oł')
            # sylables[-2] = sylables[-2].replace('u', 'uł')
            pass
        word = "ェ".join(sylables)  # 분리기호로 다시 음절들을 연결한다
        words2.append(word)
    esp_txt = " ".join(words2)

    # 각 단어별로 분리기호 ェ가 들어있는 것을 모두 제거한다.
    words = esp_txt.split(' ')
    words2 = []
    for word in words:
        sylables = word.split('ェ')  # 분리기호로 어절을 분리한다
        word = "".join(sylables)
        # word = "-".join(sylables[0:-1]) + sylables[-1] #끝에서 두번째 음절 앞에만 마이너스기호로 띄어쓴다
        words2.append(word)
    esp_txt = " ".join(words2)

    # 여기에서 온 갓 종류의 예외 처리를 수행한다
    # ok > ohk 등으로 바꾼다
    esp_words = org_esp_txt.split(" ")
    pol_words = esp_txt.split(" ")
    assert len(esp_words) == len(pol_words), "길이가 다릅니다"
    for i, esp_word in enumerate(esp_words):
        # 폴란드에서 끝에 n을 ng로 발음하는 경향이 있음.
        if len(pol_words[i]) >= 2 and pol_words[i][-2:] == "nn":  # 이미 ..nn 이면 그대로 두고
            continue
        elif pol_words[i][-1:] == "n":  # 끝에 n으로 끝나면 n을 하나 더 붙여준다
            pol_words[i] += "n"

    for i, esp_word in enumerate(esp_words):
        if esp_word in exception_pol:
            pol_words[i] = exception_pol[esp_word]
    
    pol_txt = " ".join(pol_words)

    org_esp_txt = org_esp_txt.replace(" !", "!")
    org_esp_txt = org_esp_txt.replace(" ,", ",")
    org_esp_txt = org_esp_txt.replace(" .", ".")
    org_esp_txt = org_esp_txt.replace(" ?", "?")
    # org_esp_txt = org_esp_txt.replace(" ~", "~")
    org_esp_txt = org_esp_txt.replace(" :", ":")
    org_esp_txt = org_esp_txt.replace(" ;", ";")
    org_esp_txt = org_esp_txt.replace(" (", "(")
    org_esp_txt = org_esp_txt.replace(" )", ")")
    org_esp_txt = org_esp_txt.replace(" \"", "\"")

    pol_txt = pol_txt.replace(" !", "!")
    pol_txt = pol_txt.replace(" ,", ",")
    pol_txt = pol_txt.replace(" .", ".")
    pol_txt = pol_txt.replace(" ?", "?")
    # pol_txt = pol_txt.replace(" ~", "~")
    pol_txt = pol_txt.replace(" :", ":")
    pol_txt = pol_txt.replace(" ;", ";")
    pol_txt = pol_txt.replace(" (", "(")
    pol_txt = pol_txt.replace(" )", ")")
    pol_txt = pol_txt.replace(" \"", "\"")

    org_esp_txt = org_esp_txt.strip()
    pol_txt = pol_txt.strip()

    return [org_esp_txt, pol_txt]


def get_pol_mp3_file(voicename, pol_txt, out_mp3):
    googletts.speak(pol_txt, voicename, out_mp3)


def get_esp_mp3_file(voicename, esp_txt, out_mp3):
    if voicename == 'ludoviko':
        googletts.speak(esp_txt, voicename, out_mp3)
    else:
        [esp_txt, pol_txt] = esp_to_polish(esp_txt)
        googletts.speak(pol_txt, voicename, out_mp3)


if __name__ == "__main__":
    if (len(sys.argv) < 4):
        print("Usage: %s -e 'esp_txt' 'male1'" % sys.argv[0])
        print("Usage: %s -p 'pol_txt' 'female1'" % sys.argv[0])
        sys.exit(0)
    voicename = sys.argv[3]
    if (sys.argv[1] == '-e'):
        esp_txt = sys.argv[2]
        if voicename == 'ludoviko':
            get_esp_mp3_file(voicename, esp_txt, "output.mp3")
            # googletts.speak(esp_txt, voicename, "output.mp3")
            [esp_txt, pol_txt] = esp_to_polish(esp_txt)
            print("esp_txt=%s\npol_txt=%s" % (esp_txt, pol_txt))
        else:
            [esp_txt, pol_txt] = esp_to_polish(esp_txt)
            print("esp_txt=%s\npol_txt=%s" % (esp_txt, pol_txt))
            get_pol_mp3_file(voicename, pol_txt, "output.mp3")
            # googletts.speak(pol_txt, voicename, "output.mp3")

    else:
        pol_txt = sys.argv[2]
        print("pol_txt=%s" % (pol_txt))
        get_pol_mp3_file(voicename, pol_txt, "output.mp3")
        # googletts.speak(pol_txt, voicename, "output.mp3")
